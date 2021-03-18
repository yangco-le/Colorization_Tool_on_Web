<template>
  <el-container>
    <el-header class="m-header">
      <img
        src="../assets/logo.png"
        style="height: 75px; float: left; margin-left: 10px"
      />
      <span style="float: right; margin-right: 20px">
        <el-button size="medium" type="success" plain style="margin-right: 5px" @click="colorize"
          >Start Coloring <i class="el-icon-video-play el-icon-video-right"></i>
        </el-button>
        <el-upload
          class="upload-demo inline-block"
          :show-file-list="false"
          action="/api/sketchProcess/"
          :before-upload="onBeforeUpload"
          :on-success="onSuccess"
        >
          <el-button
            size="medium"
            type="primary"
            :title="'You can only upload jpg/png files and no more than 1Mb.'"
            plain
            style="margin-right: 5px"
            >Upload <i class="el-icon-upload2 el-icon-right"></i>
          </el-button>
        </el-upload>
        <el-button size="medium" type="primary" plain @click="handleCanvas2Img"
          >Download <i class="el-icon-download el-icon-video-right"></i
        ></el-button>
      </span>
    </el-header>
    <hr />
    <el-container>
      <el-aside width="250px">
        <el-radio-group
          v-model="isCollapse"
          style="margin-bottom: 20px; margin-top: 20px"
        >
          <el-radio-button :label="false">Unfold</el-radio-button>
          <el-radio-button :label="true">Fold</el-radio-button>
        </el-radio-group>
        <el-menu
          default-active="1-4-1"
          class="el-menu-vertical-demo"
          :collapse="isCollapse"
          :default-openeds="['1', '2', '3']"
        >
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-edit"></i>
              <span slot="title" @click="handleChangeToolType(1)"><strong>Colored Brush</strong></span>
            </template>
            <el-menu-item index="1-1" @click="handleChangeToolType(1)">
              <span class="demonstration" style="margin-right: 5px">Color</span>
              <el-color-picker
                v-model="currentColor"
                style="float: right; margin-right: 20px"
              ></el-color-picker>
            </el-menu-item>
            <el-menu-item index="1-2" @click="handleChangeToolType(1)">
              <span class="demonstration">Size</span>
              <el-slider
                v-model="brushSize"
                :min="0.5"
                :max="5"
                :step="0.5"
                style="width: 70px; float: right"
              ></el-slider>
            </el-menu-item>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-remove-outline"></i>
              <span slot="title" @click="handleChangeToolType(2)"><strong>Eraser</strong></span>
            </template>
            <el-menu-item index="2-1" @click="handleChangeToolType(2);handleClearCanvas()">Clear All</el-menu-item>
            <el-menu-item index="2-2" @click="handleChangeToolType(2)">
              <span class="demonstration">Size</span>
              <el-slider
                v-model="eraserSize"
                :min="5"
                :max="50"
                :step="5"
                style="width: 70px; float: right"
              ></el-slider>
            </el-menu-item>
          </el-submenu>

          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-setting"></i>
              <span slot="title"><strong>Control</strong></span>
            </template>
            <el-menu-item index="3-1" @click="handlePrev()">Previous Step</el-menu-item>
            <el-menu-item index="3-2" @click="handleNext()">Next Step</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-main>
        <el-card shadow="hover">
          <div class="board">
            <canvas id="ctx_front" ref="ctx_front"></canvas>
            <canvas id="ctx_base" ref="ctx_base"></canvas>
            <canvas id="ctx_back" ref="ctx_back"></canvas>
          </div>
        </el-card>

        <el-card shadow="hover">
          <div class="board">
            <el-image
              style="width: 512px; height: 512px"
              v-if="res_bg"
              :src="res_bg"
              :fit="fit"></el-image>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>

export default {
  name: "ColorizationPage",
  data() {
    return {
      activeTool: 1,
      isCollapse: false,
      fileList: [],
      currentColor: "#409EFF",
      brushSize: 2.5,
      eraserSize: 25,
      background: null,
      res_bg: null,
      canvasStore: null,
      prevDis: true,
      nextDis: true,
      canDraw: false,
      canvas_front: null,
      canvas_back: null,
      canvas_base: null,
      ctx_base: null,
      ctx_front: null,
      ctx_back: null,
      currentImg: null,
    };
  },
  methods: {
    onBeforeUpload(file) {
      const isIMAGE = file.type === "image/jpeg" || file.type === "image/png";
      const isLt1M = file.size / 1024 / 1024 < 1;

      if (!isIMAGE) {
        this.$message.error("The uploaded file can only be in image format!");
      }
      if (!isLt1M) {
        this.$message.error("The size of the uploaded file cannot exceed 1MB!");
      }
      return isIMAGE && isLt1M;
    },
    onSuccess(res, file) {
      this.background = "data:image/png;base64," + res;
      this.$message.success("Uploaded successfully!");
      this.handleInitCanvas();
    },
    colorize() {
      var canvas = document.getElementById("ctx_back");
      var img = canvas.toDataURL("image/png");
      let param = new FormData();
      param.append('hint', img);
      this.$axios.post('/api/colorization/', param).then( res=>{
        this.res_bg = "data:image/png;base64," + res.data;
        // let img = new Image();
        // img.src = this.res_bg;
        // let _this = this;
        // this.canvas_res = document.getElementById("ctx_res");
        // this.ctx_res = this.canvas_res.getContext("2d");
        // img.onload = function () {
        //   // let width = parseInt(this.width);
        //   // let height = parseInt(this.height);
        //   let width = 100;
        //   let height = 100;
        //   _this.ctx_res.width = width;
        //   _this.ctx_res.height = height;
        //   _this.ctx_res.drawImage(this, 0, 0, width, height);
        // };
      })
    },
    // Clear the canvas
    handleClearCanvas() {
      this.handleInitCanvas();
    },
    // Download the image
    handleCanvas2Img() {
      var a = document.createElement('a');
      var event = new MouseEvent('click');
      a.download = 'image';
      a.href = this.res_bg;
      a.dispatchEvent(event);
    },
    // Initialize the canvas
    handleInitCanvas() {
      this.currentImg = {
        url: this.background,
        width: "",
        height: "",
        scale: 1,
        index: 0,
      };
      this.canvasStore = [this.background];
      this.prevDis = true;
      this.nextDis = true;

      // 用于绘制的画板
      this.canvas_front = document.getElementById("ctx_front");
      // 用于生成绘制后图片的画板
      this.canvas_back = document.getElementById("ctx_back");
      // 底图画板，橡皮擦除时获取像素放到绘制画板中，达到不擦出底图的效果
      this.canvas_base = document.getElementById("ctx_base");

      this.ctx_base = this.canvas_base.getContext("2d");
      this.ctx_front = this.canvas_front.getContext("2d");
      this.ctx_back = this.canvas_back.getContext("2d");
      // this.ctx_front.strokeStyle = this.currentColor;
      let img = new Image();
      img.src = this.background;
      let _this = this;
      img.onload = function () {
        let width = parseInt(this.width);
        let height = parseInt(this.height);
        _this.currentImg.width = width;
        _this.currentImg.height = height;
        _this.canvas_front.width = width;
        _this.canvas_front.height = height;
        _this.canvas_back.width = width;
        _this.canvas_back.height = height;
        _this.canvas_base.width = width;
        _this.canvas_base.height = height;
        // _this.ctx_front.drawImage(this, 0, 0, width, height);
        _this.ctx_back.drawImage(this, 0, 0, width, height);
        _this.ctx_base.drawImage(this, 0, 0, width, height);
      };
    },
    // Draw
    handleDrawCanvas(type) {
      this.canDraw = false;
      let sx, sy, mx, my;
      //鼠标按下
      let mousedown = (e) => {
        this.ctx_front.strokeStyle = this.currentColor;
        this.ctx_front.lineWidth = this.brushSize;
        e = e || window.event;             // 兼容需要
        sx = e.offsetX;
        sy = e.offsetY;
        const cbx = this.ctx_base.getImageData(
          sx - this.eraserSize / 2,
          sy - this.eraserSize / 2,
          this.eraserSize,
          this.eraserSize
        );
        this.ctx_front.moveTo(sx, sy);
        this.canDraw = true;
        switch (type) {
          case 1:
            this.ctx_front.beginPath();
            break;
          case 2:
            this.ctx_front.putImageData(
              cbx,
              e.offsetX - this.eraserSize / 2,
              e.offsetY - this.eraserSize / 2
            );
            break;
        }
      };
      let mousemove = (e) => {
        e = e || window.event;
        mx = e.offsetX;
        my = e.offsetY;
        const cbx = this.ctx_base.getImageData(
          e.offsetX,
          e.offsetY,
          this.eraserSize,
          this.eraserSize
        );
        if (this.canDraw) {
          switch (type) {
            case 1:
              this.ctx_front.lineTo(mx, my);
              this.ctx_front.stroke();
              break;
            case 2:
              this.ctx_front.putImageData(
                cbx,
                e.offsetX,
                e.offsetY
              );
              break;
          }
        }
      };
      let mouseup = () => {
        if (this.canDraw) {
          this.canDraw = false;
          this.ctx_front.closePath();
          this.handleSaveCanvasStore();
        }
      };
      this.canvas_front.onmousedown = (e) => mousedown(e);
      this.canvas_front.onmousemove = (e) => mousemove(e);
      this.canvas_front.onmouseup = (e) => mouseup(e);
      this.canvas_front.onmouseout = (e) => mouseup(e);
      this.canvas_front.onmouseleave = (e) => mouseup(e);
    },
    // Store
    handleSaveCanvasStore() {
      let url = this.canvas_front.toDataURL();
      let image = new Image();
      image.src = url;
      image.onload = () => {
        this.ctx_front.clearRect(
          0,
          0,
          this.canvas_front.width,
          this.canvas_front.height
        );
        this.ctx_front.drawImage(image, 0, 0, image.width, image.height);
        this.ctx_back.drawImage(image, 0, 0, image.width, image.height);
        const url2 = this.canvas_back.toDataURL();
        this.currentImg.url = url2;
        this.currentImg.index += 1;
        this.canvasStore.push(url2);
        this.prevDis = false;
        // console.log(this.canvasStore);
      };
    },
    /** 工具切换*/
    handleChangeToolType(type) {
      console.log(type);
      this.activeTool = type;
      this.handleDrawCanvas(type);
    },
    /** 上一步*/
    handlePrev() {
      if (this.currentImg.index > 0) {
        this.nextDis = false;
        this.currentImg.index -= 1;
        this.currentImg.index==0?this.prevDis = true:this.prevDis = false
        this.currentImg.url = this.canvasStore[this.currentImg.index];
        this.currentImg.scale = 1;
        this.handleDrawImage();
      } else {
        this.prevDis = true;
      }
    },
    /** 下一步*/
    handleNext() {
      if (this.currentImg.index<this.canvasStore.length-1) {
        this.prevDis = false;
        this.currentImg.index += 1;
        this.currentImg.index==this.canvasStore.length-1?this.nextDis = true:this.nextDis = false
        this.currentImg.url = this.canvasStore[this.currentImg.index];
        this.currentImg.scale = 1;
        this.handleDrawImage();
      } else {
        this.nextDis = true;
      }
    },
    handleDrawImage() {
      let _this = this;
      let img = new Image();
      let baseImg = new Image();
      img.src = this.currentImg.url;
      baseImg.src = this.background;
      _this.currentImg.width = _this.currentImg.width;
      _this.currentImg.height = _this.currentImg.height;
      img.onload = function() {
        _this.canvas_front.width = _this.currentImg.width;
        _this.canvas_front.height = _this.currentImg.height;
        _this.canvas_back.width = _this.currentImg.width;
        _this.canvas_back.height = _this.currentImg.height;
        _this.ctx_front.drawImage(
          this,
          0,
          0,
          _this.currentImg.width,
          _this.currentImg.height
        );
        _this.ctx_back.drawImage(
          this,
          0,
          0,
          _this.currentImg.width,
          _this.currentImg.height
        );
      };
      baseImg.onload = () => {
        _this.canvas_base.width = _this.currentImg.width;
        _this.canvas_base.height = _this.currentImg.height;
        _this.ctx_base.drawImage(
          baseImg,
          0,
          0,
          _this.currentImg.width,
          _this.currentImg.height
        );
      };
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.handleInitCanvas();
      this.handleChangeToolType(1);
    });
  },
};
</script>

<style>
.el-header {
  background-color: #ffffff;
  color: rgb(63, 58, 58);
  text-align: center;
  line-height: 80px;
  border-bottom: 1px solid rgb(211, 200, 200);
}

.m-header {
  height: 80px !important;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 240px;
  min-height: 400px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}

.el-submenu {
  background-color: rgb(255, 255, 255);
}

.board {
  position: relative;
  min-height: 30%;
}

canvas {
  width: 512px;
  height: 512px;
  position: absolute;
  margin: 0 auto;
  left: 0;
  right: 0;
  top: 0;
  float: center;
  border: 1px solid rgb(233, 229, 229);
}
#ctx_front {
  z-index: 5;
}
#ctx_back {
  z-index: 3;
}
#ctx_base {
  z-index: 1;
}

.el-card {
  width: 555px;
  height: 555px;
  margin-left: 3em;
  float: left;
}

.inline-block {
  display: inline-block;
}
</style>