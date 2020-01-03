<template>
  <div>
    <p id="game_question">Where is the {{currentWord}}?</p>
    <button id="answer_button" type="button" class="btn btn-info" v-show="!isAnswerButtonClick"
            @click="clickMeaningButton">click to get answer
    </button>
    <button type="button" class="btn btn-secondary" @click="errorModal = true">Error Submit</button>
    <audio :src="audioSrcSuccess" id="successAudio"></audio>
    <audio :src="audioSrcFail" id="failAudio"></audio>
    <p><img id="gameImg" :src="imgSrc" @click="testClick" @load="calculateRatio"/></p>
    <Modal
      v-model="errorModal"
      title="Common Modal dialog box title"
      @on-ok="errorSubmit"
      @on-cancel="errorCancel">
      <p>Username: {{username}}</p>
      <p>please input error in the box below. </p>
      <textarea id="TextareaError" rows="4" v-model="errorText"></textarea>
    </Modal>

  </div>
</template>

<script>
  import store from '../store'

  export default {
    name: 'GamePlay',
    data() {
      return {
        username: '',
        isAnswerButtonClick: false,
        words_loc: {},
        words: [],
        currentWord: '',
        currentWordCN: '',
        currentWordNum: 0,

        imgSrc: '',
        imgLoc: "static/img/Game/",
        game_img: null,

        audioSrcSuccess: 'static/audio/success.mp3',
        audioSrcFail: 'static/audio/fail.mp3',

        audioSuccess: null,
        audioFail: null,

        errorModal: false,

        errorText: '',

        heightRatio: 0,
        widthRatio: 0,
      }
    },
    components: {},

    created() {
      console.log('word game is created');
      const path = this.$route.path;
      this.game_img = path.substr(path.lastIndexOf('/') + 1);
      this.getData();
      this.imgSrc = this.imgLoc + "/" + this.game_img + ".jpg";
      this.username = store.state.username;
    },
    mounted() {
      this.audioSuccess = document.querySelector('#successAudio');
      this.audioFail = document.querySelector('#failAudio');
      console.log('audio', this.audioSuccess);
    },
    watch: {
      heightRatio: function () {
        console.log('heightRatio', this.heightRatio)
      },
      widthRatio: function () {
      }
    },
    methods: {
      calculateRatio() {
        let gameImg = document.getElementById('gameImg');
        console.log('gameImg', gameImg);
        this.heightRatio = gameImg.height / gameImg.naturalHeight;
        this.widthRatio = gameImg.width / gameImg.naturalWidth;
        console.log('heightRatio', this.heightRatio);
        console.log('widthRatio', this.widthRatio);
      },
      clickMeaningButton() {
        this.isAnswerButtonClick = true;
      },
      getData() {
        const path = '/game_word';
        this.$axios.get(path,
          {
            params: {
              game_img: this.game_img
            }
          })
          .then(response => {
            console.log(response.data);
            this.words_loc = response.data;
            for (let key in this.words_loc) {
              this.words.push(key);
            }
            console.log('game word list', this.words);
            this.isOver();
            this.currentWord = this.words[this.currentWordNum];
            console.log(this.currentWord)
          })

      },
      isOver() {
        console.log('this.currentWordNum', this.currentWordNum);
        if (this.currentWordNum >= this.words.length) {
          this.$router.push('/game')
        } else {
          this.currentWord = this.words[this.currentWordNum];
        }
      },
      testClick(e) {
        let picX = e.offsetX;
        let picY = e.offsetY;
        console.log(picX, picY);
        console.log(this.words_loc);
        let loc = this.words_loc[this.currentWord];
        console.log('loc', loc);
        for (let i = 0; i < loc.length; ++i) {
          console.log('widthRatio', this.widthRatio);
          console.log(this.widthRatio*loc[i][0],this.widthRatio*loc[i][2]);
          console.log(this.heightRatio*loc[i][1],this.heightRatio*loc[i][3]);
          if (picX > (this.widthRatio*loc[i][0]) && picX < (this.widthRatio*loc[i][2])
            && picY > (this.heightRatio*loc[i][1]) && picY < (this.heightRatio*loc[i][3])) {
            this.currentWordNum++;
            this.audioSuccess.play();
            this.isOver();
            return;
          }
        }
        this.audioFail.play();
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
  #game_question {
    font-size: 30px;
    margin-left: 300px;

  }

  #answer_button {
    margin-left: 300px;
  }

  #gameImg {
    /*width: 400px;*/
    /*height: auto;*/
    margin-left: 300px;
    margin-top: 5px;
  }

  @media screen and (max-width: 1200px) {

  }

  #TextareaError {
    width: 100%;
  }
</style>


