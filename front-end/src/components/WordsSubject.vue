<template>
  <div class="container">
    <div id="content">
      <vue-waterfall-easy :imgsArr="imgsArr" @scrollReachBottom="getData" @click="clickPic">
        <div class="img-info" slot-scope="props">
          <p class="some-info">{{props.value.info}}</p>
        </div>
      </vue-waterfall-easy>
    </div>
  </div>
</template>

<script>
  import vueWaterfallEasy from 'vue-waterfall-easy'

  export default {
    name: 'WordsSubject',
    data() {
      return {
        imgsArr: [],
        group: 0, //用于标记第几组图片的到来
      }
    },
    components: {
      vueWaterfallEasy
    },

    methods: {
      getData() {//从后端拉取数据
        const path = '/words'
        this.$axios.get(path)
          .then(response => {
            console.log(response)
            var arr = []
            for (var i = 0; i < response.data.length; i++) {
              arr.push({src: `static/img/wordsSubject/${response.data[i]}.jpg`, info: response.data[i]})
            }
            this.imgsArr = this.imgsArr.concat(arr)
            this.group++
            console.log(this.imgsArr)
          })
      },
      clickPic(event, {index, value}) {
        console.log(index, value.info)
        this.$router.push('WordsSubject/'+value.info)

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

    @media screen and (min-width:1500px){
    .vue-waterfall-easy-scroll {
      height: 600px !important;
      width: 1300px !important;
    }
  }

</style>



