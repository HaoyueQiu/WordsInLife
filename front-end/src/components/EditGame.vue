<template>
  <div class="wraper">

    <div class="btn-group-vertical">
      <div v-for="tool in toolsArr" :key="tool"
           @click="handleTools(tool)">
        <button type="button" class="btn btn-outline-dark">{{tool}}</button>
      </div>
      <div class="canvas-wraper">
        <canvas id="canvas" ref="canvas"></canvas>
      </div>

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
        editImgSrc: '',
        imgLoc: `static/img/Game/`,
        currentTool: '',
        done: false,
        fabricObj: null,
        toolsArr: ['rectangle', 'remove'],
        mouseFrom: {},
        mouseTo: {},
        moveCount: 1,
        doDrawing: false,
        fabricHistoryJson: [],
        drawingObject: null, //绘制对象
        drawColor: '#E34F51',
        drawWidth: 2,
        zoom: window.zoom ? window.zoom : 1,
      }
    },
    components: {},
    computed: {
      canvasWidth() {
        return window.innerWidth
      }
    },
    mounted() {
      //初始化canvas
      this.initCanvas()
    },
    methods: {
      initCanvas() {
        this.fabricObj = new fabric.Canvas('canvas');
        this.fabricObj.setWidth(this.canvasWidth);
        this.fabricObj.setHeight(500);
        //绑定画板事件
        this.fabricObjAddEvent()
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
            this.updateModifications(true);
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
            let object = e.target;
            this.updateModifications(true)
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
            this.updateModifications(true)
          },
        });
      },
      transformMouse(mouseX, mouseY) {
        return {x: mouseX / this.zoom, y: mouseY / this.zoom};
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
            // statements_def'
            break;
        }
        if (fabricObject) {
          this.fabricObj.add(fabricObject)
          this.drawingObject = fabricObject;
        }
      },
    },
    created() {
      this.editImgSrc = this.imgLoc + store.state.editImgSrc;
      console.log(this.editImgSrc)

    }
  }

</script>


<style>

</style>


