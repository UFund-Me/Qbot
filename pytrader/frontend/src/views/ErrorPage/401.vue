<template>
    <div class='flex flex-center'>
        <el-row class='errPage-container'>
            <el-col :span='12'>
                <h1 class='text-jumbo text-ginormous my-6'>Oops!</h1>
                gif来源
                <a href='https://zh.airbnb.com/' target='_blank'>airbnb</a>
                页面
                <h2 class='font-semibold text-2xl my-6'>你没有权限去该页面</h2>
                <h6 class='font-semibold text-xs my-6'>如有不满请联系你领导</h6>
                <router-link to='/' class='bullshit__return-home'>回首页</router-link>
            </el-col>
            <el-col :span='12'>
                <img :src='errGif' width='313' height='428' alt='Girl has dropped her ice cream.'>
            </el-col>
        </el-row>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import errGif from '/@/assets/img/401.gif'
import { useLayoutStore } from '/@/store/modules/layout'
export default defineComponent({
    name: '401',
    setup() {
        const { color } = useLayoutStore().getSetting
        
        return {
            errGif: `${errGif}?${+new Date()}`,
            ewizardClap: 'https://wpimg.wallstcn.com/007ef517-bafd-4066-aae4-6883632d9646',
            color
        }
    }
})
</script>

<style lang='postcss' scoped>
.errPage-container {
    padding-top: 100px;
    width: 800px;

    .pan-back-btn {
        background: #008489;
        color: #fff;
        border: none !important;
    }

    .pan-gif {
        margin: 0 auto;
        display: block;
    }

    .pan-img {
        display: block;
        margin: 0 auto;
        width: 100%;
    }

    .text-jumbo {
        font-size: 60px;
        font-weight: 700;
        color: #484848;
    }

    .list-unstyled {
        font-size: 14px;

        li {
            padding-bottom: 5px;
        }

        a {
            color: #008489;
            text-decoration: none;

            &:hover {
                text-decoration: underline;
            }
        }
    }

    .bullshit__return-home {
        display: block;
        float: left;
        width: 110px;
        height: 36px;
        background: v-bind(color.primary);
        border-radius: 50px;
        text-align: center;
        color: #fff;
        font-size: 14px;
        line-height: 36px;
        cursor: pointer;
        animation-name: slideUp;
        animation-duration: 0.5s;
        animation-delay: 0.3s;
        animation-fill-mode: forwards;
    }

    img {
        filter: brightness(95%);
    }
}
</style>