<template>
  <div>
    <p><img id="wordsImg" :src="imgSrc"/></p>
    <div>
      <button type="button" class="btn btn-info" v-show="!isMeaningButtonClick" @click="clickMeaningButton">click to get
        answer
      </button>
    </div>
    <p id="wordsMeaning" v-show="isMeaningButtonClick">{{currentWord}}</p>
    <p v-show="isMeaningButtonClick">{{currentWordCN}}</p>

    <div v-show="isMeaningButtonClick" class="btn-group" role="group" aria-label="Basic example">
      <button type="button" class="btn btn-success" @click="knowWord">认识</button>
      <button type="button" class="btn btn-warning" @click="uncertainWord">不确定</button>
      <button type="button" class="btn btn-danger" @click="unknowWord">不认识</button>
    </div>
  </div>


</template>

<script>
  import store from '../store.js'
  export default {
    name: 'Word',
    data() {
      return {
        isMeaningButtonClick: false,
        words: [],
        isKnow: [],//标记每个单词是否认识

        subject: '',
        currentPicNum: 0,
        currentWord: '',
        currentWordCN: '',

        imgSrc: '',
        imgLoc: "static/img/wordsSubject/",

        isOver: false,

      }
    },
    methods: {
      clickMeaningButton() {
        this.isMeaningButtonClick = true;
      },
      getData() {
        const path = '/words'
        this.$axios.get(path,
          {
            params: {
              wordsubject: this.subject,
              username:store.state.username,
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
      },

      knowWord() {
        //认识的单词就标记为已经认识不再背诵
        this.isKnow[this.currentPicNum] = true;
        this.refresh();
      }
      ,
      unknowWord() {
        //不认识的单词放到队尾继续背诵
        this.refresh();
      }
      ,
      uncertainWord() {
        //不确定的单词
        this.refresh();
      }
      ,
      refresh() {
        this.nextWord();
        this.isMeaningButtonClick = false;
        if (!this.isOver) {
          this.currentWord = this.words[this.currentPicNum]['EN'];
          this.currentWordCN = this.words[this.currentPicNum]['CN'];
          this.imgSrc = this.imgLoc + this.subject + "/" + this.currentWord + ".jpg";
        } else {
          //背完这组单词后！
          this.$router.push('/wordsSubject');
        }
      }
      ,
      nextWord() {

        let i = 0;
        const wordsLength = this.words.length

        for (; i <= wordsLength; ++i) {
          //直接这样写并不能更改currentPicNum
          // this.currentPicNum = (this.currentPicNum++)%wordsLength;
          this.currentPicNum++;
          this.currentPicNum = this.currentPicNum % wordsLength;
          if (!this.isKnow[this.currentPicNum]) {
            break;
          }
        }
        //连续已被认识过的单词，如果等于单词数目，代表这个词组已背完。
        if (i > wordsLength) {
          this.isOver = true;
        }

      }
    }
    ,
    created() {
      console.log('words is created')
      const path = this.$route.path;
      this.subject = path.substr(path.lastIndexOf('/') + 1);
      console.log(this.subject);
      this.words = [{"EN": this.subject, "CN": ''}]
      this.getData();
      this.currentWord = this.words[this.currentPicNum]['EN'];
      this.currentWordCN = this.words[this.currentPicNum]['CN'];
      this.imgSrc = this.imgLoc + this.subject + "/" + this.currentWord + ".jpg";
    }
  }

</script>


<style scoped>
  * {
    text-align: center;
    font-size: 20px;
  }

  #wordsMeaning {
    padding: 10px 0px 0px 0px;
  }

  #wordsImg {
    width: auto;
    height: 300px;
    top: 400px;
  }

  @media screen and (max-width: 1200px) {

  }

</style>


