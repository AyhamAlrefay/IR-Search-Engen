<script setup lang="ts">

</script>

<template>
  <img src="../../assets/icons/favicon.png" width="100px" height="100px" alt="">

<!--   SPINNER ORBITS-->
<!--    <div class="spinner-box">-->
<!--      <div class="blue-orbit leo">-->
<!--      </div>-->

<!--      <div class="green-orbit leo">-->
<!--      </div>-->

<!--      <div class="red-orbit leo">-->
<!--      </div>-->
<!--      <div class="rotate-image w3 leo">-->
<!--        <img src="../../assets/icons/favicon.png" width="100px" height="100px" alt="">-->
<!--      </div>-->
<!--    </div>-->
</template>

<style scoped>


@keyframes spin {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(359deg);
  }
}

@keyframes spin3D {
  from {
    transform: rotate3d(.5, .5, .5, 360deg);
  }
  to {
    transform: rotate3d(0, 0, 0, 0deg);
  }
}

@keyframes configure-clockwise {
  0% {
    transform: rotate(0);
  }
  25% {
    transform: rotate(90deg);
  }
  50% {
    transform: rotate(180deg);
  }
  75% {
    transform: rotate(270deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes configure-xclockwise {
  0% {
    transform: rotate(45deg);
  }
  25% {
    transform: rotate(-45deg);
  }
  50% {
    transform: rotate(-135deg);
  }
  75% {
    transform: rotate(-225deg);
  }
  100% {
    transform: rotate(-315deg);
  }
}

@keyframes pulse {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: .25;
    transform: scale(.75);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.rotate-image {
  animation: rotate 10s infinite linear;
}

.leo {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}


.blue-orbit {
  width: 100px;
  height: 100px;
  border: 1px solid #91daffa5;
  -webkit-animation: spin3D 3s linear .2s infinite;
}

.green-orbit {
  width: 90px;
  height: 90px;
  border: 1px solid #91ffbfa5;
  -webkit-animation: spin3D 2s linear 0s infinite;
}

.red-orbit {
  width: 80px;
  height: 80px;
  border: 1px solid #ffca91a5;
  -webkit-animation: spin3D 1s linear 0s infinite;
}

.white-orbit {
  -webkit-animation: spin3D 1s linear 0s infinite;
}


.w3 {
  transform: rotate3D(.5, 1, 2, 90deg);
}
</style>
