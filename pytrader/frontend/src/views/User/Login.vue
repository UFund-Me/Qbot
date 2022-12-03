<template>
    <div class='w-screen h-screen bg-gray-800'>
        <div class='layout-login' @keyup='enterSubmit'>
            <h3 class='text-2xl font-semibold text-gray-100 text-center mb-6'>系统登陆</h3>
            <el-form ref='ruleForm' label-position='right' label-width='80px' :model='form' :rules='rules'>
                <el-form-item class='mb-6 -ml-20' prop='name'>
                    <el-input v-model='form.name' placeholder='请输入用户名' prefix-icon='el-icon-user' />
                </el-form-item>
                <el-form-item class='mb-6 -ml-20' prop='pwd'>
                    <el-input v-model='form.pwd' placeholder='请输入密码' prefix-icon='el-icon-lock' show-password />
                </el-form-item>
                <el-form-item class='mb-6 -ml-20'>
                    <el-button type='primary' class='w-full' @click='onSubmit'>登录</el-button>
                </el-form-item>
                
                <div class='flex justify-between'>
                    <div class='text-gray-300'>
                        <p class='leading-6 text-sm'><span class='w-24 inline-block'>账号: admin</span> 密码: admin</p>
                        <p class='leading-6 text-sm'><span class='w-24 inline-block'>账号: dev</span> 密码: dev</p>
                        <p class='leading-6 text-sm'><span class='w-24 inline-block'>账号: test</span> 密码: test</p>
                    </div>
                    <div><el-button type='primary'>第三方登录</el-button></div>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue'
import { useLayoutStore } from '/@/store/modules/layout'
import { ElNotification } from 'element-plus'
import { validate } from '/@/utils/formExtend'

const formRender = () => {
    const { login } = useLayoutStore()
    let form = reactive({
        name: 'admin',
        pwd: 'admin'
    })
    const ruleForm = ref(null)
    const enterSubmit = (e:KeyboardEvent) => {
        if(e.key === 'Enter') {
            onSubmit()
        }
    }
    const onSubmit = async() => {
        let { name, pwd } = form
        if(!await validate(ruleForm)) return
        await login({ username: name, password: pwd })
        ElNotification({
            title: '欢迎',
            message: '欢迎回来',
            type: 'success'
        })
    }
    const rules = reactive({
        name: [
            { validator: (rule: any, value: any, callback: (arg0?: Error|undefined) => void) => {
                if (!value) {
                    return callback(new Error('用户名不能为空'))
                }
                callback()
            }, trigger: 'blur' 
            }
        ],
        pwd: [
            { validator: (rule: any, value: any, callback: (arg0?: Error|undefined) => void) => {
                if (!value) {
                    return callback(new Error('密码不能为空'))
                }
                callback()
            }, trigger: 'blur' 
            }
        ]
    })
    return {
        form, 
        onSubmit,
        enterSubmit,
        rules,
        ruleForm
    }
}
export default defineComponent({
    name: 'Login',
    setup() {
        return {
            labelCol: { span: 4 },
            wrapperCol: { span: 14 },
            ...formRender()
        }
    }
})
</script>

<style lang='postcss' scoped>
.layout-login {
    padding-top: 200px;
    width: 400px;
    margin: 0 auto;

    ::v-deep(.el-input__inner) {
        border: 1px solid hsla(0, 0%, 100%, 0.1);
        background: rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        color: #ddd;
    }
}

</style>