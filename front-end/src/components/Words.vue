<template>
  <div class="container">
    <div id="content">
      <vue-waterfall-easy :imgsArr="imgsArr" @scrollReachBottom="getData"></vue-waterfall-easy>
    </div>
  </div>
</template>

<script>
  import vueWaterfallEasy from 'vue-waterfall-easy'
  export default {
    name: 'Words',
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
              arr.push({src: `static/img/${response.data[i]}.jpg`})
            }
            this.imgsArr = this.imgsArr.concat(arr)
            this.group++
            console.log(this.imgsArr)
          })
      }
    },

    created() {
      this.getData()
    }
  }
</script>


<style>

  .vue-waterfall-easy-scroll {
    height: 500px !important;
  }

  .vue-waterfall-easy {
    height: 600px !important;
  }

</style>



