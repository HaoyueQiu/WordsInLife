<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-3 g-mb-40 g-mb-0--lg">
        <!-- User Image -->
        <div class="g-mb-20">
          <img src="../assets/logo.png">
        </div>

        <div class="col-sm-9">
          <!-- Username -->
          <div class="d-flex align-items-center justify-content-sm-between g-mb-5">
            <h2 v-if="user.name" class="g-font-weight-300 g-mr-10">username : {{ user.name }}</h2>
            <h2 v-else class="g-font-weight-300 g-mr-10">{{ user.username }}</h2>
          </div>
          <!-- End Username -->

          <div v-if="user.about_me">
            <div class="u-divider u-divider-db-dashed u-divider-center g-brd-gray-light-v2 g-mt-50 g-mb-20">
              <i
                class="u-divider__icon u-divider__icon--indented g-bg-gray-light-v4 g-color-gray-light-v1 rounded-circle">Me</i>
            </div>
            <p class="lead g-line-height-1_8">{{ user.about_me }}</p>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>


<script>
  import store from '../store'

  export default {
    name: 'Profile',
    data() {
      return {
        sharedState: store.state,
        user: {
          username: '',
          user_id: '',
          name: '',
          about_me: ''
        }
      }
    },
    methods: {
      getUser(username) {
        const path = '/user/${username}'
        this.$axios.get(path)
          .then((response) => {
            this.user = response.data
          })
          .catch((error) => {
            console.error(error)
          });
      }
    },
    /*
    created() {
      const username = this.$router.params.username
      this.getUser(username)
    }
  */
  }
</script>
