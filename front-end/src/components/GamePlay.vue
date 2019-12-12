<template>
  <div>
    <p id="game_question">Where is the Apple?</p>
    <button id="answer_button" type="button" class="btn btn-info" v-show="!isAnswerButtonClick"
            @click="clickMeaningButton">click to get
      answer
    </button>
    <p><img id="wordsImg" :src="imgSrc" @click="testClick"/></p>
    <div>

    </div>
  </div>
</template>

<script>
  export default {
    name: 'GamePlay',
    data() {
      return {
        isAnswerButtonClick: false,
        words: [],

        currentWord: '',
        currentWordCN: '',

        imgSrc: '',
        imgLoc: "static/img/Game/",

        isOver: false,

        game_img: null,

      }
    },

    created() {
      console.log('word game is created');
      const path = this.$route.path;
      this.game_img = path.substr(path.lastIndexOf('/') + 1);
      this.getData();
      this.imgSrc = this.imgLoc + "/" + this.game_img + ".jpg";
    },

    methods: {
      clickMeaningButton() {
        this.isAnswerButtonClick = true;
      },
      getData() {
        /*
        const path = '/words'
        this.$axios.get(path,
          {
            params: {
              wordsubject: this.subject
            }
          })
          .then(response => {
            console.log(response.data)
            this.words = this.words.concat(response.data);
          })

        for (let i = 0; i != this.words.length; ++i) {
          this.isKnow.push(false);
        }
        console.log(this.words);
        console.log(this.isKnow);
        */
      },
      testClick(e){
        console.log(e);
        let picX = e.screenX -300;
        let picY = e.screenY -400;
        console.log(picX,picY);
      },
    }
  }

</script>


<style scoped>
  #game_question {
    font-size: 30px;
    margin-left: 300px;

  }

  #answer_button {
    margin-left: 300px;
  }

  #wordsImg {
    /*width: 400px;
    height: auto;*/
    margin-left: 300px;
    top: 400px;
  }

  @media screen and (max-width: 1200px) {

  }

</style>


