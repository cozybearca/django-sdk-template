import * as $ from "jquery"
import "./form-utils.scss"
import { Ajax } from "base/clientlib"

export function init() {
    makeIntoAjaxForm($("[data-js-ajax-form]"))
    /* Need to disable globall browser's bad UX when hitting enter
        on an input submits the form */
    $(document).on(
        "keydown",
        ":input:not(textarea):not(:submit):not([data-js-on-enter-submit])",
        function (event) {
            if (event.key == "Enter") {
                event.preventDefault()
            }
        }
    )
}

export function handleDjangoRestError(
    payload: any,
    scope: HTMLElement,
    field_element_map: any = {}
) {
    console.warn(
        "handleDjangoRestError",
        "payload:",
        payload,
        "scope:",
        scope,
        "field_element_map:",
        field_element_map
    )
    const $scope = $(scope)
    resetDjangoRestError($scope)
    for (const field_name in payload) {
        const msg = payload[field_name]
        let elem: JQuery<HTMLFormElement>
        /* Locate the element to display form error */
        if (field_element_map[field_name]) {
            elem = $(field_element_map[field_name])
        } else {
            elem = $scope.find(`input[name="${field_name}"]`) as any
            if (elem.attr("type") == "radio") {
                elem = $scope.find(`input[name="${field_name}"]:checked`) as any
            }
            if (elem.length) {
                console.debug(
                    `Found element to display error for field: ${field_name}`,
                    elem[0]
                )
            } else {
                console.debug(
                    `Did not find element to display error for field: ${field_name}`,
                    elem
                )
                // if the field doesn't exit, create a fake field
                elem = $scope.find(`button, input[type="submit"]`) as any
                console.debug("...fallback to submit button", elem)
            }
            if (!elem.length) {
                console.error(
                    `Could not find any html element to display error for field: ${field_name}`
                )
            }
        }
        elem.addClass("data-js-has-error")
        elem[0].setCustomValidity(msg)
        elem[0].reportValidity()
        elem.one("change", function (evt) {
            resetDjangoRestErrorForFields($(this as any))
        })
    }
    if (payload["non_field_errors"] != undefined) {
        $scope.find(`button, input[type="submit"]`).each((idx, elem: any) => {
            if (elem[0].setCustomValidity) {
                elem[0].setCustomValidity(payload["non_field_errors"])
                elem[0].reportValidity()
            }
        })
    }
}

function resetDjangoRestErrorForFields(fields: JQuery<HTMLFormElement>) {
    fields.removeClass("data-js-has-error").each((idx, elem) => {
        if (elem.setCustomValidity) {
            elem.setCustomValidity("")
            elem.reportValidity()
        }
    })
}

function resetDjangoRestError(scope: JQuery<HTMLElement>) {
    resetDjangoRestErrorForFields(scope.find("input, button, textarea, select") as any)
}

/**
 * makeIntoAjaxForm
 *
 * Expect the form to either have an action attribute, or has a button of
 * type=submit that has a formaction attribute. All restful http methods are
 * supported. Each input submitted must have the name attribute.
 *
 * @param String form_selector
 * @param Callback onsuccess
 * @param Callback onerror
 */
export function makeIntoAjaxForm(
    form_selector: JQuery<HTMLElement>,
    onsuccess = (data: any) => {
        window.location.reload()
    },
    onerror = (data: any) => {}
) {
    return form_selector.each(function () {
        const form = $(this) as JQuery<HTMLFormElement>
        const buttons_set = form.find('button[type="submit"]')
        if (!buttons_set.length) {
            console.error('cannot find button[type="submit" in this form', form)
        }
        buttons_set.on("click", async function (evt) {
            evt.preventDefault()
            resetDjangoRestError(form)
            const button = $(this)
            let url = button.attr("formaction")
            if (!url) {
                console.log("[formaction] not found on button", button)
                url = form.attr("action")
                if (!url) {
                    console.log("[action] not found on form", form)
                    console.error(
                        "cannot determine form submit url, submit event:",
                        evt
                    )
                    return
                }
            }
            let method = button.attr("formmethod")
            if (!method) {
                console.log("[formmethod] not found on button", button)
                method = form.attr("method")
                if (!method) {
                    console.log("[method] not found on form", form)
                    console.error(
                        "cannot determine form submit method, submit event:",
                        evt
                    )
                    return
                }
            }

            console.log("ajax form submit event", evt)

            const send: any = {}
            for (const kvp of form.serializeArray()) {
                send[kvp.name] = kvp.value
            }
            try {
                const response = await Ajax.request(
                    method.toLocaleUpperCase() as any,
                    url,
                    send
                )
                onsuccess(response)
            } catch (error) {
                handleDjangoRestError(error.responseJSON, form[0])
                onerror(error.responseJSON)
            }
        })
    })
}
