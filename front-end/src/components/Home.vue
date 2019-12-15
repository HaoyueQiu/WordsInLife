<template>
  <div class="container">
    <h1>words in life 手册</h1>
    <p>WIL的想法来源于我们很难记忆日常物体词汇，因此根据其特点设计了该应用...</p>
    <p><img class="introImg" id="img0" src="static/img/introduction/intro0.jpg"/></p>
    <p><img class="introImg" id="img1" src="static/img/introduction/intro1.jpg"/></p>
    <p><img class="introImg" id="img2" src="static/img/introduction/intro2.jpg"/></p>
    <p><img class="introImg" id="img3" src="static/img/introduction/intro3.jpg"/></p>
    <p><img class="introImg" id="img4" src="static/img/introduction/intro4.jpg"/></p>
    <p><img class="introImg" id="img5" src="static/img/introduction/intro5.jpg"/></p>
    <p><img class="introImg" id="img6" src="static/img/introduction/intro6.jpg"/></p>
  </div>
</template>

<script>
  import Alert from './Alert'

  export default {
    name: 'Home',  //this is the name of the component
    components: {},
    data() {
      return {
        imgNum: [0, 1, 2, 3, 4, 5],
        imgLoc: 'static/img/introduction/intro'


      }
    }
  }
</script>


<style scoped>
  .introImg {
    padding: 20px 0px 20px 0px;
    text-align: center;
  }

  #img0, #img1, #img4, #img5, #img6 {
    max-width: 800px;
  }

  #img2, #img3 {
    height: 300px !important;
  }
</style>
