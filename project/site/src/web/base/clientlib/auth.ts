import { Ajax } from "django-client-framework"

const LOGIN_VIA_SMS = "/api/v1/login/sms_auth"
const LOGOUT = "/api/v1/logout"
const LOGIN_WITH_GOOGLE = "/api/v1/login/google_auth"
const LOGIN_VIA_PWD = "/api/v1/login/pwd_auth"

export class LoginAPI {
    public via_sms(params: {
        country_code: string
        mobile_number: string
        code_text: string
    }) {
        return Ajax.request("POST", LOGIN_VIA_SMS, params)
    }
    public via_google_signin(id_token: string) {
        return Ajax.request("POST", LOGIN_WITH_GOOGLE, {
            id_token: id_token,
        })
    }
    public via_pwd(params: { email_address: string; password: string }) {
        return Ajax.request("POST", LOGIN_VIA_PWD, params)
    }
    public is_authenticated(): boolean {
        return window as any["is_authenticated"]
    }
}

export class LogoutAPI {
    public async logout() {
        return Ajax.request("POST", LOGOUT, {})
    }
}
