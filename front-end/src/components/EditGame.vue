<template>
  <div class="wraper">
    <div class="controlPanel">
      <div class="btn-group-vertical">
        <div v-for="tool in toolsArr" :key="tool"
             @click="handleTools(tool)">
          <button type="button" class="btn btn-outline-dark">{{tool}}</button>
        </div>
      </div>
    </div>

    <div class="canvas-wrapper">
      <canvas id="canvas" ref="canvas"></canvas>
    </div>
    <div id="img1">
      <img :src="editImgSrc" id="my-img" >
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
        imgObj: {src: ''},
        editImgSrc: 'static/img/Game/fruits0.jpeg',
        imgLoc: `static/img/Game/`,
        currentTool: '',//当前选择的工具
        done: false,
        fabricObj: null,//绘制的图像
        toolsArr: ['rectangle', 'remove'],
        mouseFrom: {},
        mouseTo: {},
        moveCount: 1,
        doDrawing: false,
        drawingObject: null, //绘制对象
        drawColor: '#E34F51',
        drawWidth: 2,
        zoom: window.zoom ? window.zoom : 1,
      }
    },
    components: {},
    computed: {
      canvasWidth() {
        return window.innerWidth;
      },
      canvasHeight(){
        return window.innerHeight;
      }
    },
    created() {
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
        console.log(this.fabricObj);
        let img0 = 'static/img/Game/fruits0.jpeg';
        //加载图片
        let imgElement = document.getElementById('my-img');
        let imgInstance = new fabric.Image(imgElement, {
        });

        //添加背景
        this.fabricObj.setBackgroundImage(imgInstance);
        console.log(this.canvasWidth);
        this.fabricObj.setWidth(imgInstance.width);
        this.fabricObj.setHeight(imgInstance.height);
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
            if (e.target._objects) {
              //多选删除
              var etCount = e.target._objects.length;
              for (var etindex = 0; etindex < etCount; etindex++) {
                this.fabricObj.remove(e.target._objects[etindex]);
              }
            } else {
              //单选删除
              this.fabricObj.remove(e.target);
            }
            this.fabricObj.discardActiveObject(); //清楚选中框
          },
        });
      },
      resetObj() {
        this.fabricObj.selectable = false;
        this.fabricObj.selection = false;
        this.fabricObj.skipTargetFind = true;
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
          default:
            break;
        }
      },
      drawing() {
        console.log(this.drawingObject)
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
              fill: "rgba(255, 255, 255, 0)"
            });
            break;
          case 'remove':
            break;
          default:
            break;
        }
        if (fabricObject) {
          this.fabricObj.add(fabricObject)
          this.drawingObject = fabricObject;
        }
      },
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
  #my-img{
    width: 0.1px;
    height:0.1px;
    display: none;
  }
  #img1{
    position: absolute;
    margin-left:0px;
  }
</style>

