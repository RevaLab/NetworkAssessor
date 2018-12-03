<template>
  <div id="app">
    <div class="nav-bar-wrapper" v-on:click="navigateHome">
        <div class="nav-bar">
            <div class="network-icon-and-page-title">
                <img class="network-icon" src="static/network-icon.jpg">
                <h4>Network Assessor</h4>
                <h2>beta</h2>
            </div>
            <div class="sinai-logo">
                <img src="static/MSSMLogo.png">
            </div>
        </div>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
    export default {
        components: {},
        methods: {
            navigateHome() {
               this.$router.go('/');
            }
        }
    }

</script>

<style>

/* START STYLE RESET */
  html, body, header, nav, h1, a,
  ul, li, strong, main, button, i,
  section, img, div, h2, h3, h4, h5, p, form,
  fieldset, label, input, textarea,
  span, article, footer, time, small {
    margin: 0;
    padding: 0;
    border: 0;
    outline: 0;
    font: sans-serif;
    color: inherit;
    text-align: inherit;
    text-decoration: inherit;
    vertical-align: inherit;
    box-sizing: inherit;
    background: transparent;
  }

  ul, li {
    list-style: none;
  }

  img {
    display: block;
    width: 100%;
    height: auto;
  }

  input[type="password"],
  input[type="email"],
  input[type="text"],
  input[type="submit"],
  textarea,
  button {
    -webkit-appearance: none;
    -moz-appearance: none;
  }

  button,
  input[type="submit"] {
    cursor: pointer;
  }
/* END RESET */

.nav-bar-wrapper {
    margin: 30px auto;
    /*width: */
    max-width: 80%;
    min-width: 450px;
    cursor: pointer;
}

.nav-bar {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    min-width: 100%;
}

.network-icon-and-page-title {
    display: flex;
    flex-direction: row;
    margin-right: 100px;
    flex-shrink: 0;
}

.nav-bar h4 {
  font-size: 2em;
  /*text-align: center;*/
  padding: .6em 0;
  /*height: 80px;*/
    font-weight: bold;
}

.nav-bar h2 {
    margin-top: 20px;
}

.nav-bar .network-icon {
    height: 80px;
    width: 80px;
    margin-right: 10px;
}

.nav-bar .sinai-logo {
    height: 69px;
    width: 353px;
    min-width: 353px;
    /*overflow-x: hidden;*/
}

.content {
  height: calc(100vh - 100px);
}

#app{
  /*overflow: hidden;*/
    /*max-height: 100vh;*/
    /*position: relative;*/
}
</style>
