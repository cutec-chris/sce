document.addEventListener('promet-before-loaded',function(){
    AFRAME.registerComponent('sce-item', {
        dependencies: ['gltf-model'],
        schema: {
            asset: {type: 'string'},
        },
        init: function () {
            let s = this.data.asset;
            s = s.substring(s.lastIndexOf("/"));
            s = '/contents/'+this.data.asset+s.toLowerCase()+'_'+'10'+'.glb';
            console.log(s);
            this.el.setAttribute('gltf-model', s);
        },
    });
});