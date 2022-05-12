#version 330

const int maxSteps = 50;
const float stepSize = 0.2;
const int numSamples = 256;
const int numBounces = 3;

const vec3 skyCol = vec3(5.0);

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec4 p3d_Color;

out vec3 color;

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform sampler3D map_tex;

struct RayHit {
    vec3 col, pos, norm;
    bool out_bounds;
};


vec3 sampleMapTex(vec3 pos) {
    return texture(map_tex, vec3(pos.x / 6.0, (6.0 - pos.z) / 6.0, pos.y / 5.0)).xyz;
}
float random21(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}
vec3 GetRandomVec3(vec3 st) {
    float rand = random21(st.yx);
    float rand2 = random21(st.xz);
    float rand3 = random21(st.zy);
    vec3 r = vec3(rand, rand2, rand3) * 2.0 - 1.0;
    return normalize(r);
}
vec3 getRayNorm(vec3 pos, vec3 prev_pos) {
    vec3 f_pos = floor(pos);
    vec3 f_prev_pos = floor(prev_pos);

    return normalize(f_prev_pos - f_pos);
}

RayHit castRay(vec3 dir, vec3 pos) {
    vec3 ray_dir = dir * stepSize;
    vec3 ray_pos = pos;
    RayHit ray_hit;

    for (int i = 0; i < maxSteps; i++) {
        ray_pos += ray_dir;

        vec3 tex_col = sampleMapTex(ray_pos);

        if (tex_col != vec3(0, 0, 0)) {
            ray_hit.col = tex_col;
            ray_hit.pos = ray_pos;
            ray_hit.norm = getRayNorm(ray_pos, ray_pos - ray_dir);
            ray_hit.out_bounds = false;

            if (ray_pos.y > 5.0) ray_hit.out_bounds = true;
            break;
        }
    }
    return ray_hit;
}

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

    vec3 fragPos = round(vec3(p3d_ModelMatrix * p3d_Vertex) * 100.0) / 100.0;
    vec3 norm = normalize(p3d_Normal);

    vec3 albedo = vec3(0.0);
    for (int i = 0; i < numSamples; i++) {
        vec3 ray_pos = fragPos;
        vec3 ray_norm = norm;
        vec3 ray_albedo = vec3(0.0);
        vec3 ray_light = vec3(0.0);

        for (int j = 0; j < numBounces; j++) {
            vec3 rvec = GetRandomVec3(fragPos + j + i);

            vec3 dir = mix(ray_norm, rvec, 0.49);

            RayHit ray = castRay(dir, ray_pos);

            ray_pos = ray.pos;
            ray_norm = ray.norm;
            ray_albedo += ray.col * pow(1.0 - (float(j) / float(numBounces)), 2.0);
            
            if (ray.out_bounds) {
                ray_light = skyCol;
                break;
            }
        }
        ray_albedo /= float(numBounces);

        albedo += (ray_albedo * ray_light);
    }
    
    albedo /= float(numSamples);

    color = albedo * vec3(p3d_Color);
}
