<template>
  <div class="container">
    <vue-waterfall-easy :imgsArr="imgsArr" @scrollReachBottom="getData" @click="clickPic">
      <div class="img-info" slot-scope="props">
        <p class="some-info">{{props.value.info}}</p>
      </div>
    </vue-waterfall-easy>
    <input type="file" id="choseFile" @change="onFileChange">
    <label for="choseFile" id="editButton" class="btn btn-outline-primary">Edit Game</label>
  </div>
</template>

<script>
  import vueWaterfallEasy from 'vue-waterfall-easy'
  import EditGame from './EditGame'
  import store from '../store.js'

  export default {
    name: 'Game',
    data() {
      return {
        editImgSrc: '',
        imgLoc: `static/img/Game/`,
        imgsArr: [],
        group: 0,
      }
    },
    components: {
      vueWaterfallEasy
    },

    methods: {
      onFileChange(event) {
        this.editImgSrc = event.target.files[0].name;
        console.log(this.editImgSrc);
        store.state.editImgSrc = this.editImgSrc;
        this.$router.push('editGame');
      },
      getData() {//从后端拉取数据
        const path = '/game';
        this.$axios.get(path)
          .then(response => {
            console.log(response);
            var arr = [];
            for (var i = 0; i < response.data.length; i++) {
              arr.push({src: this.imgLoc + response.data[i]['EN'] + '.jpeg', info: response.data[i]['word_subject']})
            }
            this.imgsArr = this.imgsArr.concat(arr);
            this.group++;
            console.log(this.imgsArr);
          })
      },
      clickPic(event, {index, value}) {
        console.log(index, value.info);
        this.$router.push('game/' + value.info);
      }
    },

    created() {
      this.getData()
    }
  }

</script>


<style>
  #choseFile {
    width: 0.1px;
    height: 0.1px;
  }

  #editButton {
    position: fixed;
    bottom: 100px;
    right: 80px;
  }

  .vue-waterfall-easy {
    height: 600px !important;
  }

  @media screen and (max-width: 1500px) {
    .vue-waterfall-easy-scroll {
      height: 500px !important;
      width: 780px !important;
    }
  }

  @media screen and (min-width: 1500px) {
    .vue-waterfall-easy-scroll {
      height: 600px !important;
      width: 1300px !important;
    }
  }
</style>



