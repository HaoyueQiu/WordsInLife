<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        <img src="../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        Words In Life
      </router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="nav nav-tab">
        <!--<div class="collapse navbar-collapse"> -->
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">

          <!-- 导航栏 -->
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home <span class="sr-only">(current)</span></router-link>
          </li>
        </ul>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">


          <li class="nav-item">
            <router-link to="/wordsSubject" class="nav-link">Words</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/game" class="nav-link">Game</router-link>
          </li>
        </ul>

        <form class="form-inline navbar-left mr-auto">
          <input class="form-control mr-sm-2" type="search" placeholder="Search">
          <!-- 暂时先禁止提交，后续实现搜索再改回 type="submit" -->
          <button class="btn btn-outline-success my-2 my-sm-0" type="button">Search</button>
        </form>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
          <li class="nav-item">
            <a class="nav-link disabled" href="#">Messages</a>
          </li>
          <li class="nav-item">
            <router-link to="/profile" class="nav-link">Profile</router-link>
          </li>
          <li class="nav-item">
            <p class="nav-link" @click="errorModal = true">Error/Suggest</p>
            <Modal
              v-model="errorModal"
              title="Error or Suggestion"
              @on-ok="errorSubmit"
              @on-cancel="errorCancel">
              <p>Username: {{username}}</p>
              <p>please input error or suggestion in the box below. </p>
              <textarea id="TextareaError" rows="4" v-model="errorText"></textarea>
            </Modal>
          </li>
          <li class="nav-item">
            <a v-on:click="handlerLogout" class="nav-link" href="#">Logout</a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav navbar-right">
          <li class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
        </ul>

      </div>
    </div>
  </nav>

</template>

<script>
  import store from '../store.js'

  export default {
    name: 'Navbar',  //this is the name of the componen
    data() {
      return {
        sharedState: store.state,
        username: store.state.username,
        errorModal: false,

        errorText: '',
      }
    },
    methods: {
      handlerLogout(e) {
        store.logoutAction()
        //this.$toasted.show('you have been logged out.',{icon:'fingerprint'})
        this.$router.push('/login')
      },
      errorSubmit() {
        const path = '/findingError';
        const payload = {
          username: this.username,
          errorText: this.errorText,
        };
        this.$axios.post(path, payload)
          .then(response => {
            this.errorText = '';
            console.log(response);
          })
      },
      errorCancel() {
        this.errorText = '';
      }
    }
  }
</script>


<style scoped>

  #TextareaError {
    width: 100%;
  }
</style>
