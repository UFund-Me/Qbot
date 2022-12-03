import { Ref, unref } from 'vue'

/**
 * 表单校验
 * @param ref 节点
 * @param isGetError 是否获取错误项
 */
export async function validate(ref: Ref|any, isGetError = false):Promise<boolean | {valid: boolean, object: any}> {
    const validateFn = unref(ref).validate
    return new Promise(resolve => validateFn((valid:boolean, object: any) => isGetError ? resolve({ valid, object }) : resolve(valid)))
}

/**
 * 对部分表单字段进行校验的方法
 * @param ref 节点
 * @param props 字段属性
 */
export async function validateField(ref: Ref|any, props: Array<string> | string):Promise<string> {
    const validateFieldFn = unref(ref).validateField
    return new Promise(resolve => validateFieldFn(props, (errorMessage: string) => resolve(errorMessage)))
}

/**
 * 重置表单
 * @param ref 节点
 */
export function resetFields(ref: Ref|any):void {
    const resetFieldsFn = unref(ref).resetFields
    resetFieldsFn()
}

/**
 * 移除表单项的校验结果
 * @param ref 节点
 * @param props 字段属性
 */
export function clearValidate(ref: Ref|any, props?: Array<string> | string):void {
    const clearValidateFn = unref(ref).clearValidate
    props ? clearValidateFn(props) : clearValidateFn()
}