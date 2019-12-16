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
    <audio v-show="isMeaningButtonClick" :src="audioSrc" id="wordAudio">audio</audio>

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

        audioSrc: '',
        audioLoc: 'static/audio/',

        isOver: false,

      }
    },
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
      this.audioSrc = this.audioLoc + this.subject + "/" + this.currentWord + "--_gb_1.mp3";
    },
    beforeDestroy() {
      //背完这组单词后,将times等数据存回数据库
      console.log('this.words', this.words);
      const path = '/words';
      const payload = {
        words: this.words,
        username: store.state.username,
      }
      this.$axios.post(path, payload)
        .then(response => {
        })
    },
    methods: {
      clickMeaningButton() {
        this.isMeaningButtonClick = true;
        let audio = document.querySelector('#wordAudio');
        audio.play();
      },
      getData() {
        const path = '/words'
        this.$axios.get(path,
          {
            params: {
              wordsubject: this.subject,
              username: store.state.username,
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
        //单词的熟练度改变，其规则为认识的话加1/times熟练度，其中若times > 5,则加0.2
        let p_tmp = this.words[this.currentPicNum]['proficiency'];
        this.words[this.currentPicNum]['times']++;
        if (this.words[this.currentPicNum]['times'] > 5) {
          p_tmp += 0.2;
        } else {
          p_tmp += 1 / this.words[this.currentPicNum]['times'];
        }
        console.log('current word info', this.words[this.currentPicNum])
        p_tmp = this.min_max(0, 1, p_tmp);
        this.words[this.currentPicNum]['proficiency'] = p_tmp;
        this.refresh();
      },
      // num is in [a,b]
      min_max(a, b, num) {
        if (num < a) {
          num = a;
        } else if (num > b) {
          num = b;
        }
        return num;
      },
      unknowWord() {
        //不认识的单词放到队尾继续背诵
        //单词的熟练度改变，其规则为不认识的话则减0.2
        let p_tmp = this.words[this.currentPicNum]['proficiency'];
        p_tmp -= 0.2;
        this.words[this.currentPicNum]['times']++;
        p_tmp = this.min_max(0, 1, p_tmp);
        this.words[this.currentPicNum]['proficiency'] = p_tmp;
        this.refresh();
      }
      ,
      uncertainWord() {
        //不确定的单词
        //熟练度不改变
        this.words[this.currentPicNum]['times']++;
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
          this.audioSrc = this.audioLoc + this.subject + "/" + this.currentWord + "--_gb_1.mp3";
          console.log(this.audioSrc)
        } else {

          this.$router.push('/wordsSubject');
        }
      },

      nextWord() {

        let i = 0;
        const wordsLength = this.words.length

        for (; i <= wordsLength; ++i) {
          //直接这样写并不能更改currentPicNum
          // this.currentPicNum = (this.currentPicNum++) % wordsLength;
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


