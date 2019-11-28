<template>
  <div class = "container">
    <alert
      v-if="sharedState.is_new"
      v-bind:variant="alertVariant"
      v-bind:message="alertMessage">
    </alert>
    <h1>Sign In</h1>
    <div class="row">
      <!--bootstrap 的栅栏布局，能够简便的通过预定义的类做出布局，最多分为12列。
       xs (phones), sm (tablets), md (desktops), and lg (larger desktops)
       可以通过不同的类定义在不同的大小的界面上
       -->
      <div class="col-md-4">
        <!--创建表单，@是v-on:的简写，它用于监听DOM事件。
        .prevent是为v-on提供的事件修饰符。@submit.prevent提交事件不再重载界面
        -->
        <form @submit.prevent="onSubmit">
          <div class="form-group">
            <!--for属性能够让label与表单元素绑定，当指向lable时，表单元素也可以获得焦点
            https://www.w3school.com.cn/tags/att_label_for.asp
            https://www.cnblogs.com/lixlib/archive/2011/10/19/label-for.html
            -->
            <label for="username">Username</label>
            <input type="text" v-model="loginForm.username" class="form-control" v-bind:class="{'is-invalid': loginForm.usernameError}" id="username" placeholder="">
            <div v-show="loginForm.usernameError" class="invalid-feedback">{{ loginForm.usernameError }}</div>
          </div>
          <!--form-group 便捷创造bootstrap表单https://getbootstrap.com/docs/4.3/components/forms/-->
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" v-model="loginForm.password" class="form-control" v-bind:class="{'is-invalid': loginForm.passwordError}" id="password" placeholder="">
            <div v-show="loginForm.passwordError" class="invalid-feedback">{{ loginForm.passwordError }}</div>
          </div>
          <button type="submit" class="btn btn-primary">Sign In</button>
        </form>
      </div>
    </div>
    <br>
    <p> New User? <router-link to="/register">Click to Register!</router-link></p>
    <p>
      Forgot your password?
      <!--重置密码功能
        。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
      -->
      <a href="#">Click to Reset It!</a>
    </p>
  </div>
</template>

<script>
  import axios from 'axios'
  import Alert from './Alert'
  import store from '../store.js'
  export default {
    name:'Login',
    components:{
      alert:Alert
    },
    data(){
      return {
        sharedState: store.state,
        alertVariant: 'info',
        alertMessage: 'Congratulations, welcome to Words In life!',
        loginForm: {
          username:'',
          password:'',
          submitted:false,
          errors:0,
          usernameError:null,
          passwordError:null
        }
      }
    },
    methods:{
      onSubmit(e) {
        console.log('come in')
      //e 是干嘛的？！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！1
        this.loginForm.submitted = true  // 先更新状态
        this.loginForm.errors = 0
        if (!this.loginForm.username) {
          this.loginForm.errors++
          this.loginForm.usernameError = 'Username required.'
        } else {
          this.loginForm.usernameError = null
        }
        if (!this.loginForm.password) {
          this.loginForm.errors++
          this.loginForm.passwordError = 'Password required.'
        } else {
          this.loginForm.passwordError = null
        }
        if (this.loginForm.errors > 0) {
         // 表单验证没通过时，不继续往下执行
          return false
        }
        //通过 axios 连接前后端，能够调用后端API，以下实现了auth，获得token
        //const path = 'http://localhost:5000/api/tokens'
        const path = '/tokens'
        // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
        this.$axios.post(path,{},{
          auth:{
            'username':this.loginForm.username,
            'password':this.loginForm.password
          }
        }).then((response)=>{
          //handle success
          window.localStorage.setItem('token',response.data.token)
          // store.resetNotNewAction()
          store.loginAction()
          this.$toasted.success(`Welcome! ${name}!`, { icon: 'fingerprint' })
          console.log("hi")
          if(typeof  this.$route.query.redirect == 'undefined'){
            this.$router.push('/')
          }else{
            this.$router.push(this.$route.query.redirect)
          }
        })
          .catch((error)=>{
            //handle error
            console.log(error.response)
            /*
            if(error.response.status == 401){
              this.loginForm.usernameError = 'Invalid username or password'
              this.loginForm.usernameError = 'Invalid username or password'
            }else{
              console.log(error.response)
            }*/
          })

    }
  }
}
</script>
