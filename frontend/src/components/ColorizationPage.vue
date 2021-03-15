<template>
  <el-container>
    <el-header class="m-header">
      <img
        src="../assets/logo.png"
        style="height: 75px; float: left; margin-left: 10px"
      />
      <span style="float: right; margin-right: 20px">
        <el-button size="medium" type="success" plain style="margin-right: 5px"
          >Start Coloring <i class="el-icon-video-play el-icon-video-right"></i
        ></el-button>
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
              <span slot="title"><strong>Colored Brush</strong></span>
            </template>
            <el-menu-item index="1-1">
              <span class="demonstration" style="margin-right: 5px">Color</span>
              <el-color-picker
                v-model="currentColor"
                style="float: right; margin-right: 20px"
              ></el-color-picker>
            </el-menu-item>
            <el-menu-item index="1-2">
              <span class="demonstration">Size</span>
              <el-slider
                v-model="brushSize"
                :min="1"
                :max="10"
                :step="1"
                style="width: 70px; float: right"
              ></el-slider>
            </el-menu-item>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-remove-outline"></i>
              <span slot="title"><strong>Eraser</strong></span>
            </template>
            <el-menu-item index="2-1">Clear All</el-menu-item>
            <el-menu-item index="2-2">
              <span class="demonstration">Size</span>
              <el-slider
                v-model="eraserSize"
                :min="1"
                :max="10"
                :step="1"
                style="width: 70px; float: right"
              ></el-slider>
            </el-menu-item>
          </el-submenu>

          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-setting"></i>
              <span slot="title"><strong>Control</strong></span>
            </template>
            <el-menu-item index="3-1">Previous Step</el-menu-item>
            <el-menu-item index="3-2">Next Step</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-main>
        <el-card shadow="hover">
          <div class="board">
            <canvas id="ctx_front"></canvas>
            <canvas id="ctx_base"></canvas>
            <canvas id="ctx_back"></canvas>
          </div>
        </el-card>

        <el-card shadow="hover">
          <div class="board"></div>
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
      isCollapse: false,
      fileList: [],
      currentColor: "#409EFF",
      brushSize: 3,
      eraserSize: 3,
      background: null,
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
    // Clear the canvas
    handleClearCanvas() {
      this.handleInitCanvas();
    },
    // Download the image
    handleCanvas2Img() {
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
      this.ctx_front.strokeStyle = this.currentColor;
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
  width: 30em;
  height: 30em;
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
  width: 33em;
  height: 33em;
  margin-left: 3em;
  float: left;
}

.inline-block {
  display: inline-block;
}
</style>