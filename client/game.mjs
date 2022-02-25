export function staticAsset(aPath,aProps) {
    let obj = document.createElement('a-entity');
    obj.setAttribute('sce-item','asset',aPath);
    for (var prop in aProps) {
        obj.setAttribute(prop,aProps[prop]);
    }
    return obj;
}
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