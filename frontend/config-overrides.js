/* config-overrides.js */
const path = require('path');

module.exports = function override(config, env) {
  // Extend Webpack config here
  config.resolve.extensions.push('.mjs');
  config.module.rules.push({
    test: /\.mjs$/,
    include: /node_modules/,
    type: 'javascript/auto'
  });
  return config;
};