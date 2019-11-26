import Vue from 'vue'
import Router from 'vue-router'
import Ping from '@/components/Ping'

Vue.use(Router)

//暴露路由接口
export default new Router({
  routes: [
    {
      path: '/',
      name: 'Ping',
      // component 代表加载到相应路由上后所使用的组件
      component: Ping
    }
  ]
})
