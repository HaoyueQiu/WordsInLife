<template>
  <div id="app">
    <navbar></navbar>
    <router-view />
  </div>
</template>

<script>
  import Navbar from './components/Navbar'
  //import Login from './components/Login'
  //export 和 export default均用于导出，但是export在引用时要加花括号，而export default可以直接被引用
  //https://www.jianshu.com/p/edaf43e9384f
  export default {
    name: 'App',
    //运训组件模板递归地调用自身，且便于调试，报错时会报名字，方便定位。
    // https://cn.vuejs.org/v2/api/#name
    components:{
      navbar:Navbar,
    }
  }

</script>

<style>
  /*
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
  */
</style>
