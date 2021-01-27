import * as ko from "knockout"
import "home.scss"

export function init() {
    const view_model = {
        list: ko.observableArray([-1, 0, 1].map(ko.observable)) as ko.ObservableArray<
            ko.Observable<number>
        >,
        plus() {
            for (var i = 0; i < view_model.list().length; i++) {
                var item = view_model.list()[i]
                item(item() + 1)
            }
        },
        minus() {
            for (var i = 0; i < view_model.list().length; i++) {
                var item = view_model.list()[i]
                item(item() - 1)
            }
        },
        add() {
            view_model.list.push(ko.observable(0))
        },
        remove() {
            view_model.list.pop()
        },
    }
    ko.applyBindings(view_model)
}
