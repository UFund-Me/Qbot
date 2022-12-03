import { App, DirectiveBinding } from 'vue'
import { checkPermission, IPermissionType } from '/@/utils/permission'

const actionPermission = (el:HTMLElement, binding:DirectiveBinding) => {
    const value:Array<string> = typeof binding.value === 'string' ? [binding.value] : binding.value
    const arg:IPermissionType = binding.arg === 'and' ? 'and' : 'or'
    if(!checkPermission(value, arg)) {
        el.parentNode && el.parentNode.removeChild(el)
    }
}

export default (app:App<Element>):void => {
    app.directive('action', {
        mounted: (el, binding) => actionPermission(el, binding)
    })
}