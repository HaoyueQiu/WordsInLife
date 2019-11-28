import axios from 'axios'
export default {
  debug: true,
  state: {
    is_authenticated: window.localStorage.getItem('token') ? true : false,
    // 用户登录后，就算刷新页面也能再次计算出 user_id，通过获取的token JSON文件进行解析
    user_id: 0,
    // is_new: false
  },
  loginAction(){
    if(this.debug){
      console.log('loginAction is triggered')
    }
    this.state.is_authenticated = true
    const path = '/tokens'
    axio.get(path,{'token':window.localStorage.getItem('token')},{
      auth: {
        'username': this.loginForm.username,
        'password': this.loginForm.password
      }
    }).then((response)=>{
      this.state.user_id = response.data.user_id
      console.log(this.state.user_id)
    })
  },
  logoutAction(){
    if(this.debug) console.log('logoutAction is triggered')
    window.localStorage.removeItem('token')
    this.state.is_authenticated = false
    this.state.user_id = 0
  },
  /*
  setNewAction () {
    if (this.debug) { console.log('setNewAction is triggered') }
    this.state.is_new = true
  },
  resetNotNewAction () {
    if (this.debug) { console.log('resetNotNewAction is triggered') }
    this.state.is_new = false
  }
  */
}
