<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{msg}}</button>
  </div>
</template>

<script>
  import  axios from 'axios'
  /*
  axios:https://cn.vuejs.org/v2/cookbook/using-axios-to-consume-apis.html
  axios可用于访问api并展示其数据
  */

  export default {
    name: 'Ping',
    data() {
      return {
        msg: 'hi'
      }
    },
    methods: {
      getMessage() {
        const path = 'http://localhost:5000/api/ping'
        axios.get(path)
        /*
          .then()方法是异步执行,当.then()前的方法执行完后再执行then()内部的程序
          这样能够避免数据没获取到等问题
         */
        /*
        * 箭头函数是简化的函数表达，此外它的this总是指向词法作用域，即外层调用者的位置。
        * https://www.liaoxuefeng.com/wiki/1022910821149312/1031549578462080
        *  */
          .then((res) => {
            this.msg = res.data;
          })
          .catch((error) => {
            console.error(error)
          })
      }
    },
    created() {
      this.getMessage()
    }
  }
</script>
