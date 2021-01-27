from logging import getLogger

from django.contrib.auth import password_validation
from django.utils.translation import gettext as _
from django_client_framework import exceptions as e
from django_client_framework import serializers as s
from src.common import models as m

LOG = getLogger(__name__)


class UserSerializer(s.DelegateSerializer):
    @s.generate_jsonschema(for_model=m.User)
    class ReadUpdateUser(s.DCFModelSerializer):
        class Meta:
            model = m.User
            fields = [
                "id",
                "first_name",
                "last_name",
                "username",
            ]

    @s.generate_jsonschema(for_model=m.User)
    class UpdatePassword(s.Serializer):
        new_password = s.CharField()
        new_password_again = s.CharField()
        verification_code = s.CharField()

        def validate_new_password(self, value):
            password_validation.validate_password(
                value,
                user=self.instance,
                password_validators=[
                    password_validation.MinimumLengthValidator(),
                    password_validation.UserAttributeSimilarityValidator(),
                    password_validation.NumericPasswordValidator(),
                    password_validation.CommonPasswordValidator(),
                ],
            )
            return value

        def validate(self, attr):
            if attr["new_password"] != attr["new_password_again"]:
                raise e.ValidationError(
                    dict(
                        new_password_again=_(
                            "Password was inconsistent. Make sure you type the same password again."
                        )
                    )
                )
            return attr

        def validate_verification_code(self, verification_code):
            vc = m.VerificationCode.filter_unexpired(
                text=verification_code, action=m.VerificationCode.Action.CHANGE_PASSWORD
            )
            if vc.exists():
                return vc
            else:
                raise e.ValidationError(
                    dict(verification_code=_("Incorrect validation code"))
                )

        def update(self, user, validated_data):
            validated_data["verification_code"].delete()
            user.set_password(validated_data["new_password"])
            user.save()
            return user

    @s.generate_jsonschema(for_model=m.User)
    class UpdateEmailAddress(s.Serializer):
        password = s.CharField(required=False)
        new_email_address = s.CharField()
        verification_code = s.CharField()

        def validate_new_email_address(self, new_email_address):
            email = m.Email.objects.filter(address=new_email_address).first()
            if email and email.verified:
                LOG.debug(f"conflig user {self.instance}, {email.user}")
                raise e.ValidationError(
                    dict(
                        new_email_address=_(
                            f'The email address "{new_email_address}" is used by another account.'
                            " Please first permanently disable that account."
                        )
                    )
                )
            else:
                return new_email_address

        def validate(self, attr):
            vc = m.VerificationCode.filter_unexpired(
                text=attr["verification_code"],
                email__address=attr["new_email_address"],
                action=m.VerificationCode.Action.VERIFY_EMAIL,
            )

            # check verification code
            if vc.exists():
                attr.update({"verification_code": vc})
            else:
                raise e.ValidationError(
                    dict(verification_code=_("Incorrect validation code"))
                )

            """
            Verification code must be validated before password
            """
            # if user has password set, then password is required
            if self.instance.has_usable_password():
                if "password" not in attr:
                    raise e.ValidationError(dict(password="This field is required."))
                elif not self.instance.check_password(attr["password"]):
                    raise e.ValidationError(dict(password="Incorrect password"))

            return attr

        def update(self, user, validated_data):
            validated_data["verification_code"].delete()
            new_email_address = validated_data["new_email_address"]
            email = m.Email.objects.get(address=new_email_address)
            user.email = email
            user.save()
            return user

    @s.generate_jsonschema(for_model=m.User)
    class UpdateMobileNumber(s.Serializer):
        password = s.CharField(required=False)
        verification_code = s.CharField()
        new_country_code = s.IntegerField()
        new_mobile_number = s.CharField()

        def validate(self, attr):
            mobile = m.Mobile.objects.filter(
                country_code=attr["new_country_code"], number=attr["new_mobile_number"]
            ).first()
            if mobile:
                if mobile.verified:
                    raise e.ValidationError(
                        dict(
                            new_mobile_number=_(
                                "This mobile number is used by another account."
                                " Please first permanently disable that account."
                            )
                        )
                    )

            # check verification code
            vc = m.VerificationCode.filter_unexpired(
                text=attr["verification_code"],
                mobile__country_code=attr["new_country_code"],
                mobile__number=attr["new_mobile_number"],
                action=m.VerificationCode.Action.VERIFY_MOBILE,
            )
            if vc.exists():
                attr.update({"verification_code": vc})
            else:
                raise e.ValidationError(
                    dict(verification_code=_("Incorrect validation code"))
                )

            """
            Verification code must be validated before password
            """
            # if user has password set, then password is required
            if self.instance.has_usable_password():
                if "password" not in attr:
                    raise e.ValidationError(dict(password="This field is required."))
                elif not self.instance.check_password(attr["password"]):
                    raise e.ValidationError(dict(password="Incorrect password"))

            return attr

        def update(self, user, validated_data):
            mobile = m.Mobile.objects.get(
                country_code=validated_data["new_country_code"],
                number=validated_data["new_mobile_number"],
            )
            validated_data["verification_code"].delete()
            user.mobile = mobile
            user.save()
            return user

    @s.generate_jsonschema(for_model=m.User)
    class InactivateAccount(s.Serializer):
        is_active = s.BooleanField()
        password = s.CharField(required=False)
        verification_code = s.CharField()

        def validate(self, attr):
            user = self.instance
            verification_code = m.VerificationCode.filter_unexpired(
                mobile__user=user,
                action=m.VerificationCode.Action.DISABLE_ACCOUNT,
                text=attr["verification_code"],
            ).first()
            if not verification_code:
                verification_code = m.VerificationCode.filter_unexpired(
                    email__user=user,
                    action=m.VerificationCode.Action.DISABLE_ACCOUNT,
                    text=attr["verification_code"],
                ).first()
            if not verification_code:
                raise e.ValidationError(
                    dict(verification_code="Incorrect verification code.")
                )

            attr.update({"verification_code": verification_code})

            if user.has_usable_password():
                password = attr.get("password", None)
                if not user.check_password(password):
                    raise e.ValidationError(dict(password="Incorrect password"))

            return attr

        def update(self, user, validated_data):
            validated_data["verification_code"].delete()
            user.is_active = validated_data["is_active"]
            user.save()
            return user

    def get_update_delegate_class(self, user, initial_data, prevalidated_data):
        if "is_active" in initial_data:
            return self.InactivateAccount, False
        if "new_password" in initial_data:
            return self.UpdatePassword, False
        elif "new_email_address" in initial_data:
            return self.UpdateEmailAddress, False
        elif "new_mobile_number" in initial_data:
            return self.UpdateMobileNumber, False
        else:
            return self.ReadUpdateUser, True

    def get_read_delegate_class(self, instance):
        return self.ReadUpdateUser
