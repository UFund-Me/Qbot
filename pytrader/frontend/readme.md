
<p align="center">
  <img width="320" src="https://images.hsianglee.cn/elementPlusAdmin/title.png">
</p>

<p align="center">
    <a href="https://github.com/vuejs/vue-next">
        <img src="https://img.shields.io/badge/vue3-3.0.7-brightgreen.svg" alt="vue">
    </a>
    <a href="https://github.com/element-plus/element-plus">
        <img src="https://img.shields.io/badge/elementPlus-1.0.2beta.35-brightgreen.svg" alt="element-plus">
    </a>
    <a href="https://github.com/vitejs/vite">
        <img src="https://img.shields.io/badge/vite-2.1.2-brightgreen.svg" alt="vite">
    </a>
    <a href="https://github.com/microsoft/TypeScript">
        <img src="https://img.shields.io/badge/typescript-4.1.3-brightgreen.svg" alt="typescript">
    </a>
    <a href="https://github.com/postcss/postcss">
        <img src="https://img.shields.io/badge/postcss-8.2.2-brightgreen.svg" alt="postcss">
    </a>
    <a href="https://github.com/hsiangleev/element-plus-admin/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license">
    </a>
</p>


## 简介

[element-plus-admin](https://github.com/hsiangleev/element-plus-admin) 是一个后台前端解决方案，它基于 [vue-next](https://github.com/vuejs/vue-next) 和 [element-plus](https://github.com/element-plus/element-plus)实现。它使用了最新的前端技术栈vite，typescript和postcss构建，内置了 动态路由，权限验证，皮肤更换，提供了丰富的功能组件，它可以帮助你快速搭建中后台产品原型。

- [在线预览](https://element-plus-admin.hsianglee.cn/)

- [Gitee](https://gitee.com/hsiangleev/element-plus-admin)

## 前序准备

你需要在本地安装 [node](http://nodejs.org/) 和 [git](https://git-scm.com/)。本项目技术栈基于 [ES2015+](http://es6.ruanyifeng.com/)、[vue-next](https://github.com/vuejs/vue-next)、[typescript](https://github.com/microsoft/TypeScript)、[vite](https://github.com/vitejs/vite)、[postcss](https://github.com/postcss/postcss) 和 [element-plus](https://github.com/element-plus/element-plus)，所有的请求数据都使用[Mock.js](https://github.com/nuysoft/Mock)进行模拟，提前了解和学习这些知识会对使用本项目有很大的帮助。

<p align="center">
    <img width="900" src="https://images.hsianglee.cn/elementPlusAdmin/element-plus-admin.png">
</p>

## 开发

```bash
# 克隆项目
git clone https://github.com/hsiangleev/element-plus-admin.git

# 进入项目目录
cd element-plus-admin

# 安装依赖
npm install

# 启动服务
npm run dev
```

浏览器访问 http://localhost:3002

## 发布

```bash
# 发布
npm run build

# 预览
npm run preview
```

## 其它

```bash
# eslint代码校验
npm run eslint

# stylelint代码校验
npm run stylelint
```

## vscode扩展

1. 使用johnsoncodehk.volar，并禁用vetur，支持template代码里面的数据类型提示

## 浏览器

**目前仅支持现代浏览器**

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>IE / Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>Chrome | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" alt="Safari" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>Safari |
| --------- | --------- | --------- | --------- |
| Edge | last 2 versions | last 2 versions | last 2 versions |

## 捐赠

如果你觉得这个项目帮助到了你，你可以帮作者买一杯果汁表示鼓励 :tropical_drink:</br>
![donate](https://images.hsianglee.cn/pay.png?v=0.0.1)

## License

[MIT](https://github.com/hsiangleev/element-plus-admin/blob/master/LICENSE)

Copyright (c) 2020-present hsiangleev
