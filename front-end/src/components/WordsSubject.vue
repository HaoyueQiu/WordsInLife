<template>
  <div class="container">
    <div id="content">
      <vue-waterfall-easy :imgsArr="imgsArr" @scrollReachBottom="getData" @click="clickPic">
        <div class="img-info" slot-scope="props">
          <p class="some-info">{{props.value.info['wordsubject']}} {{props.value.info['complete_ratio']}}%</p>
        </div>
      </vue-waterfall-easy>
    </div>
  </div>
</template>

<script>
  import vueWaterfallEasy from 'vue-waterfall-easy'
  import store from '../store.js'
  export default {
    name: 'WordsSubject',
    data() {
      return {
        imgLoc:`static/img/wordsSubject/`,
        imgsArr: [],
        group: 0, //用于标记第几组图片的到来
      }
    },
    components: {
      vueWaterfallEasy
    },

    methods: {
      getData() {//从后端拉取数据
        const path = '/wordSubject'
        this.$axios.get(path,{
          params:{
            username:store.state.username
          }
        })
          .then(response => {
            console.log('response',response)
            var arr = []
            console.log(response.data)
            for (var i = 0; i < response.data.length; i++) {
              arr.push({src: this.imgLoc + response.data[i]['wordsubject'] + '/'+`${response.data[i]['wordsubject']}.jpg`,
                info: {'wordsubject':response.data[i]['wordsubject'],'complete_ratio':response.data[i]['complete_ratio']}});
            }
            this.imgsArr = this.imgsArr.concat(arr)
            this.group++
            console.log(this.imgsArr)
          })
      },
      clickPic(event, {index, value}) {
        console.log(index, value.info)
        this.$router.push('WordsSubject/'+value.info['wordsubject'])
      }
    },

    created() {
      this.getData()
    }
  }
</script>


<style>
  .vue-waterfall-easy {
    height: 600px !important;
  }
  @media screen and (max-width: 1500px){
    .vue-waterfall-easy-scroll {
      height: 500px !important;
      width: 780px !important;
    }
  }
  /*(min-resolution: 1.25dppx)*/
    @media screen and (min-width:1500px) {
    .vue-waterfall-easy-scroll {
      height: 600px !important;
      width: 1300px !important;
    }
  }


</style>



