- Last tested 1.20.80
- This program creates resource packs that project image pixels onto block geometry for building Minecraft pixel art
- v0.0.4 changes:
  - Changed to ujson library for speed improvement
- The created pack is client side only, and uses an armor stand to render projection
- Projection blocks are colored directly from the image pixel colors, allowing the player to substitute block types in game
- Projection will render from the coordinates entered during pack creation. Place an armor stand within render distance of the player, and within view of the pack coordinates
- If the armor stand is out of render distance, the projection will de-render also. Place another armor stand close to the player to render the projection again
- Face the armor stand in different directions to rotate the projection. The center of rotation is the pack coordinates

![pixel_projection_2](https://github.com/bud-aj29/BE_Pixel_Projection/assets/99773087/9e4d5542-f42a-4f27-9ca0-5e0eead4e314)
