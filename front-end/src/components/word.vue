<template>
  <div>
    <p><img id="wordsImg" src="static/img/animal.jpg"/></p>
    <div>
    <button type="button" class="btn btn-info" v-show="!isMeaningButtonClick" @click="clickMeaningButton">click to get answer</button>
    </div>
    <p id="wordsMeaning" v-show="isMeaningButtonClick">Animal</p>
    <p v-show="isMeaningButtonClick">动物</p>

    <div v-show="isMeaningButtonClick" class="btn-group" role="group" aria-label="Basic example">
      <button type="button" class="btn btn-success">认识</button>
      <button type="button" class="btn btn-warning">不确定</button>
      <button type="button" class="btn btn-danger">不认识</button>
    </div>
  </div>


</template>

<script>
  export default {
    name: 'Word',
    data() {
      return {
        isMeaningButtonClick: false,
        words:[],
        subject:'',
      }
    },
    methods: {
      clickMeaningButton(){
        this.isMeaningButtonClick = true
        console.log(this.isMeaningButtonClick)
        console.log(this.$route.path)
      }
    },
    created() {
      console.log(this.$route.path)
    }
  }

</script>


<style>
  * {
    text-align: center;
  }

  #wordsMeaning {
    padding: 10px 0px 0px 0px;
  }

  #wordsImg {
    width: 200px;
    height: auto;
    top: 400px;
  }

  @media screen and (max-width: 1200px) {

  }

</style>


