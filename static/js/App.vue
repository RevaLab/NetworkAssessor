<template>
  <div id="app">
    <div class="nav-bar">
      <h3>GO Network and Pathway Analysis</h3>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

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

.nav-bar h3 {
  font-size: 1.5em;
  text-align: center;
  padding: .5em 0;
  height: 60px;
}

.content {
  height: calc(100vh - 100px);
}

#app{
  overflow: hidden;
}
</style>
