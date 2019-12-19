<template>
  <div class="wraper">
    <div class="controlPanel">
      <div class="btn-group-vertical">
        <div v-for="tool in toolsArr" :key="tool"
             @click="handleTools(tool)">
          <button type="button" class="buttonCSS btn btn-outline-dark">{{tool}}</button>
        </div>
        <form @submit.prevent="onSubmit">

          <!--form-group 便捷创造bootstrap表单https://getbootstrap.com/docs/4.3/components/forms/-->
          <div class="form-group">
            <input id="word_now" v-model="currentWord" placeholder="word" class="form-control">
            <div >{{ wordInfo }}</div>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>

    <div class="canvas-wrapper">
      <canvas id="canvas" ref="canvas"></canvas>
    </div>


    <div id="img1">
      <img :src="editImgSrc" id="my-img">
    </div>
  </div>
</template>

<script>
  import store from '../store.js'
  import {fabric} from 'fabric'


  export default {
    name: 'EditGame',
    data() {
      return {
        game_img: '',
        editImgSrc: 'static/img/Game/fruits0.jpeg',
        imgLoc: `static/img/Game/`,
        currentTool: '',//当前选择的工具
        done: false,
        fabricObj: null,//绘制的图像
        toolsArr: ['rectangle', 'remove', 'clear'],
        mouseFrom: {},
        mouseTo: {},
        moveCount: 1,
        doDrawing: false,
        drawingObject: null, //绘制对象
        drawColor: '#E34F51',
        drawWidth: 2,
        zoom: window.zoom ? window.zoom : 1,
        currentWord: '',
        mouseFromList: [],
        mouseToList: [],
        imgInstance: null,
        wordInfo: '',
      }
    },
    components: {},
    computed: {
      canvasWidth() {
        return window.innerWidth;
      },
      canvasHeight() {
        return window.innerHeight;
      }
    },
    created() {
      const loc = store.state.editImgSrc.indexOf('.');
      this.game_img = store.state.editImgSrc.substr(0, loc);
      console.log(this.game_img);
      this.editImgSrc = this.imgLoc + store.state.editImgSrc;
      console.log(this.editImgSrc)
    },
    mounted() {
      //初始化canvas
      this.initCanvas()
    },
    methods: {
      initCanvas() {
        this.fabricObj = new fabric.Canvas('canvas', {});
        //加载图片
        let imgElement = document.getElementById('my-img');
        this.imgInstance = new fabric.Image(imgElement, {});

        //添加背景
        this.fabricObj.setBackgroundImage(this.imgInstance);
        this.fabricObj.setWidth(this.imgInstance.width);
        this.fabricObj.setHeight(this.imgInstance.height);
        //绑定画板事件
        this.fabricObjAddEvent();
      },
      //时间监听
      fabricObjAddEvent() {
        this.fabricObj.on({
          'mouse:down': (o) => {
            this.mouseFrom.x = o.pointer.x;
            this.mouseFrom.y = o.pointer.y;
            this.doDrawing = true;
          },
          'mouse:up': (o) => {
            this.mouseTo.x = o.pointer.x;
            this.mouseTo.y = o.pointer.y;
            this.drawingObject = null;
            this.moveCount = 1;
            this.doDrawing = false;
            let fromTemp = this.deepClone(this.mouseFrom);
            let toTemp = this.deepClone(this.mouseTo);
            this.mouseFromList.push(fromTemp);
            this.mouseToList.push(toTemp);
          },
          'mouse:move': (o) => {
            if (this.moveCount % 2 && !this.doDrawing) {
              //减少绘制频率
              return;
            }
            this.moveCount++;
            this.mouseTo.x = o.pointer.x;
            this.mouseTo.y = o.pointer.y;
            this.drawing();
          },
          //对象移动时间
          'object:moving': (e) => {
            e.target.opacity = 0.5;
          },
          'object:modified': (e) => {
            e.target.opacity = 1;
          },
          'selection:created': (e) => {
            console.log(e);
            if (e.target._objects) {
              //多选删除
              var etCount = e.target._objects.length;
              for (var etindex = 0; etindex < etCount; etindex++) {
                this.fabricObj.remove(e.target._objects[etindex]);
              }
            } else {
              console.log(e.target);
              //单选删除
              this.fabricObj.remove(e.target);
            }
            this.fabricObj.discardActiveObject(); //清除选中框
          },
        });
      },
      resetObj() {
        this.fabricObj.selectable = false;
        this.fabricObj.selection = false;
        this.fabricObj.skipTargetFind = true;
      },
      setClearState() {

        this.mouseFromList = [];
        this.mouseToList = [];
        // fabricObj.clear 会把包括背景在内的东西都清空，因此再把背景加回去。
        this.fabricObj = new fabric.Canvas('canvas', {});
        //添加背景
        console.log('imgInstance',this.imgInstance);
        this.fabricObj.setBackgroundImage(this.imgInstance);
        this.fabricObj.setWidth(this.imgInstance.width);
        this.fabricObj.setHeight(this.imgInstance.height);
        console.log(this.fabricObj);
        this.fabricObjAddEvent();

      },

      handleTools(tools) {
        this.currentTool = tools;
        this.fabricObj.isDrawingMode = false;
        this.resetObj();
        switch (tools) {
          case 'remove':
            this.fabricObj.selection = true;
            this.fabricObj.skipTargetFind = false;
            this.fabricObj.selectable = true;
            break;
          case 'clear':
            console.log(this.fabricObj);
            this.fabricObj.clear();
            console.log(this.fabricObj);
            this.setClearState();
            break;
          default:
            break;
        }
      },
      drawing() {
        if (this.drawingObject) {
          this.fabricObj.remove(this.drawingObject)
        }
        let fabricObject = null;
        switch (this.currentTool) {
          case 'rectangle': //矩形
            let path = "M " +
              this.mouseFrom.x +
              " " +
              this.mouseFrom.y +
              " L " +
              this.mouseTo.x +
              " " +
              this.mouseFrom.y +
              " L " +
              this.mouseTo.x +
              " " +
              this.mouseTo.y +
              " L " +
              this.mouseFrom.x +
              " " +
              this.mouseTo.y +
              " L " +
              this.mouseFrom.x +
              " " +
              this.mouseFrom.y +
              " z";
            fabricObject = new fabric.Path(path, {
              left: this.mouseFrom.x,
              top: this.mouseFrom.y,
              stroke: this.drawColor,
              strokeWidth: this.drawWidth,
              fill: "rgba(255, 255, 255, 0)",
            });
            break;
          case 'remove':
            break;
          default:
            break;
        }
        if (fabricObject) {
          this.fabricObj.add(fabricObject);
          this.drawingObject = fabricObject;
        }
      },
      onSubmit() {
        this.wordInfo='';
        console.log('submit word');
        console.log(this.mouseFromList, this.mouseToList);
        console.log(this.currentWord);
        const path = '/game_word';
        const payload = {
          word: this.currentWord,
          game_img: this.game_img,
          mouseFromList: this.mouseFromList,
          mouseToList: this.mouseToList,
        };
        console.log(payload);
        this.$axios.post(path, payload)
          .then((response) => {
            console.log(response)
            this.wordInfo = 'you submit this word successfully!';
          })
          .catch((error) => {
              // handle error
              console.log(error.response.data.message);
              this.wordInfo = error.response.data.message['word'];
              console.log(this.wordInfo);
            }
          );
        this.currentWord='';
        this.handleTools('clear');
      },
      deepClone(obj) {
        //JS数组浅拷贝怎么办，使用JSON转化以下再转化回去，这时候得到深拷贝的内容
        let _obj = JSON.stringify(obj),
          objClone = JSON.parse(_obj);
        return objClone;
      }
    },

  }
</script>


<style>
  .controlPanel {
    width: 100px;
    height: 100%;
    margin-left: 200px;
    position: fixed;
  }

  .canvas-wrapper {
    position: absolute;
    margin-left: 300px;
  }

  #my-img {
    width: 0.1px;
    height: 0.1px;
    display: none;
  }

  #word_now {
    border: 1px solid #000000;
  }

  #img1 {
    position: absolute;
    margin-left: 0px;
  }

  .buttonCSS{
    width:100px;
    text-align: left;
  }
</style>

