import Vue from 'vue'
import Router from 'vue-router'
import Ping from '@/components/Ping'
import Home from '@/components/Home'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Profile from '@/components/Profile'
import WordsSubject from '@/components/WordsSubject'
import Word from '@/components/Word'
import Game from '@/components/Game'
import EditGame from '@/components/EditGame'
import GamePlay from '@/components/GamePlay'

Vue.use(Router)

//暴露路由接口
const router =  new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      // component 代表加载到相应路由上后所使用的组件
      component: Home,
      meta:{
        requireAuth:true
      }
    },
    {
      path:'/login',
      name:'Login',
      component:Login
    },
    {
      path:'/register',
      name:'Register',
      component:Register
    },
        {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path:'/wordsSubject',
      name:'WordsSubject',
      component:WordsSubject
    },
    {
      path:'/wordsSubject/:subject',
      name:'words',
      component:Word
    },
    {
      path:'/game',
      name:'game',
      component:Game,
    },
    {
      path:'/game/:game_pic',
      name:'gamePlay',
      component:GamePlay,
    },
    {
      path:'/editGame',
      name:'EditGame',
      component:EditGame,
    },
  ]
})


//https://router.vuejs.org/zh/guide/advanced/navigation-guards.html#%E5%85%A8%E5%B1%80%E5%89%8D%E7%BD%AE%E5%AE%88%E5%8D%AB
//导航守卫，以下主要用于判断是否为已登录状态，未登录则请求登录
router.beforeEach((to,from,next)=>{
  const token = window.localStorage.getItem('token')
  if(to.matched.some(record => record.meta.requiresAuth) &&(!token|| token === null)){
    next({//未登录的用户重定向到登录界面。
    path: '/login',
    query: {redirect: to.fullPath}
    })
  }else if(token && to.name == 'Login') {
    //对于已经登录的用户，如果他还要去扽等各路界面那么就进行拦截
    next({
    path: from.fullPath
    })
  }else {
    next()
  }
})


export default router
