<template>
  <div class="container">
    <h1> hello </h1>
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
        group: 0
      }
    },
    components: {
      vueWaterfallEasy
    },

    methods: {
      getData() {

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

        /*
          var subject = ['fruit', 'animal', 'furniture','exercise','vegetable','bathroom']
          for (var i = 0; i < subject.length; i++) {
            this.imgsArr.push({src: `static/img/${subject[i]}.jpg`})
          }*/
        console.log(this.imgsArr)
      }

    },
    created() {
      this.getData()
    }
  }
</script>

<style>

  .vue-waterfall-easy {
    position: fixed !important;
  }
</style>
