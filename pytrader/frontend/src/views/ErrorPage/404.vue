<template>
    <div class='wscn-http404-container'>
        <div class='wscn-http404'>
            <div class='pic-404'>
                <img class='pic-404__parent' :src='err404' alt='404'>
                <img class='pic-404__child left' :src='errCloud' alt='404'>
                <img class='pic-404__child mid' :src='errCloud' alt='404'>
                <img class='pic-404__child right' :src='errCloud' alt='404'>
            </div>
            <div class='bullshit'>
                <div class='bullshit__oops'>OOPS!</div>
                <div class='bullshit__info'>
                    All rights reserved
                    <a class='bullshit__info-link' href='https://wallstreetcn.com' target='_blank'>wallstreetcn</a>
                </div>
                <div class='bullshit__headline'>{{ message }}</div>
                <div class='bullshit__info'>
                    Please check that the URL you entered is correct, or click the button below to return to the homepage.
                </div>
                <router-link to='/' class='bullshit__return-home'>Back to home</router-link>
            </div>
        </div>
    </div>
</template>
<script lang='ts'>
import { defineComponent } from 'vue'
import { useLayoutStore } from '/@/store/modules/layout'

import err404 from '/@/assets/img/404.png'
import errCloud from '/@/assets/img/404_cloud.png'

export default defineComponent({
    name: '404',
    setup() {
        const { color } = useLayoutStore().getSetting
        return {
            err404,
            errCloud,
            message: 'The webmaster said that you can not enter this page...',
            color
        }
    }
})
</script>

<style lang='postcss' scoped>
.wscn-http404-container {
    transform: translate(-50%, -50%);
    position: absolute;
    top: 40%;
    left: 50%;
}

.wscn-http404 {
    position: relative;
    width: 1200px;
    padding: 0 50px;
    overflow: hidden;

    .pic-404 {
        position: relative;
        float: left;
        width: 600px;
        overflow: hidden;

        &__parent {
            width: 100%;
        }

        &__child {
            position: absolute;

            &.left {
                width: 80px;
                top: 17px;
                left: 220px;
                opacity: 0;
                animation-name: cloudLeft;
                animation-duration: 2s;
                animation-timing-function: linear;
                animation-fill-mode: forwards;
                animation-delay: 1s;
            }

            &.mid {
                width: 46px;
                top: 10px;
                left: 420px;
                opacity: 0;
                animation-name: cloudMid;
                animation-duration: 2s;
                animation-timing-function: linear;
                animation-fill-mode: forwards;
                animation-delay: 1.2s;
            }

            &.right {
                width: 62px;
                top: 100px;
                left: 500px;
                opacity: 0;
                animation-name: cloudRight;
                animation-duration: 2s;
                animation-timing-function: linear;
                animation-fill-mode: forwards;
                animation-delay: 1s;
            }

            @keyframes cloudLeft {
                0% {
                    top: 17px;
                    left: 220px;
                    opacity: 0;
                }

                20% {
                    top: 33px;
                    left: 188px;
                    opacity: 1;
                }

                80% {
                    top: 81px;
                    left: 92px;
                    opacity: 1;
                }

                100% {
                    top: 97px;
                    left: 60px;
                    opacity: 0;
                }
            }

            @keyframes cloudMid {
                0% {
                    top: 10px;
                    left: 420px;
                    opacity: 0;
                }

                20% {
                    top: 40px;
                    left: 360px;
                    opacity: 1;
                }

                70% {
                    top: 130px;
                    left: 180px;
                    opacity: 1;
                }

                100% {
                    top: 160px;
                    left: 120px;
                    opacity: 0;
                }
            }

            @keyframes cloudRight {
                0% {
                    top: 100px;
                    left: 500px;
                    opacity: 0;
                }

                20% {
                    top: 120px;
                    left: 460px;
                    opacity: 1;
                }

                80% {
                    top: 180px;
                    left: 340px;
                    opacity: 1;
                }

                100% {
                    top: 200px;
                    left: 300px;
                    opacity: 0;
                }
            }
        }
    }

    .bullshit {
        position: relative;
        float: left;
        width: 300px;
        padding: 30px 0;
        overflow: hidden;

        .bullshit__info-link {
            color: v-bind(color.primary);
        }

        &__oops {
            font-size: 32px;
            font-weight: bold;
            line-height: 40px;
            color: v-bind(color.primary);
            opacity: 0;
            margin-bottom: 20px;
            animation-name: slideUp;
            animation-duration: 0.5s;
            animation-fill-mode: forwards;
        }

        &__headline {
            font-size: 20px;
            line-height: 24px;
            color: #222;
            font-weight: bold;
            opacity: 0;
            margin-bottom: 10px;
            animation-name: slideUp;
            animation-duration: 0.5s;
            animation-delay: 0.1s;
            animation-fill-mode: forwards;
        }

        &__info {
            font-size: 13px;
            line-height: 21px;
            color: grey;
            opacity: 0;
            margin-bottom: 30px;
            animation-name: slideUp;
            animation-duration: 0.5s;
            animation-delay: 0.2s;
            animation-fill-mode: forwards;
        }

        &__return-home {
            display: block;
            float: left;
            width: 110px;
            height: 36px;
            background: v-bind(color.primary);
            border-radius: 100px;
            text-align: center;
            color: #fff;
            opacity: 0;
            font-size: 14px;
            line-height: 36px;
            cursor: pointer;
            animation-name: slideUp;
            animation-duration: 0.5s;
            animation-delay: 0.3s;
            animation-fill-mode: forwards;
        }

        @keyframes slideUp {
            0% {
                transform: translateY(60px);
                opacity: 0;
            }

            100% {
                transform: translateY(0);
                opacity: 1;
            }
        }
    }
}
</style>