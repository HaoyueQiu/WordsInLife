<template>
  <div class="setting">
    <label>word difficulity</label>
     <RadioGroup v-model="word_difficulity" @on-change="change_word_diff" vertical>
        <Radio label="1">
            <span>难度一：常用词</span>
        </Radio>
        <Radio label="2">
            <span>难度二: 一般用词</span>
        </Radio>
        <Radio label="3">
            <span>难度三: 中国人较少熟悉度的词</span>
        </Radio>
    </RadioGroup>
<!--    <Slider v-model="word_difficulity" min="1" max="5" step="1" show-input="true" show-stops="true"-->
<!--            on-change="change_word_diff"></Slider>-->
  </div>
</template>

<script>
  import store from '../store.js'

  export default {
    name: "setting",
    data() {
      return {
        word_difficulity: 0,
      }
    },
    created(){
      this.word_difficulity = store.state.word_difficulity;
    },
    methods: {
      change_word_diff() {
        store.state.word_difficulity = this.word_difficulity;
        console.log(this.word_difficulity)
      }
    }
  }
</script>

<style scoped>
.setting{
  width:60%;

}
</style>
