#version 330

const int maxSteps = 50;
const float stepSize = 0.2;
const int numSamples = 8;
const int numBounces = 3;
const float maxLightIntensity = 2.0;

in vec3 normal;
in vec4 color;
in vec3 fragPos;

out vec4 fragColor;

uniform sampler3D map_a;
uniform sampler3D map_e;
uniform vec3 map_size;


struct RayHit {
    vec3 col, pos, norm, light;
};


vec3 sampleATex(vec3 pos) {
    return texture(map_a, vec3(pos.x / map_size.x, (map_size.z - pos.z) / map_size.z, pos.y / map_size.y)).xyz;
}
float sampleETex(vec3 pos) {
    return texture(map_e, vec3(pos.x / map_size.x, (map_size.z - pos.z) / map_size.z, pos.y / map_size.y)).x;
}
float random21(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}
vec3 GetRandomVec3(vec3 st) {
    float rand = random21(st.yx * st.z);
    float rand2 = random21(st.xz * st.y);
    float rand3 = random21(st.zy * st.x);
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
    ray_hit.light = vec3(0.0);

    for (int i = 0; i < maxSteps; i++) {
        ray_pos += ray_dir;

        vec3 a_tex_col = sampleATex(ray_pos);

        if (a_tex_col != vec3(0, 0, 0)) {
            ray_hit.col = a_tex_col;
            ray_hit.pos = ray_pos;
            ray_hit.norm = getRayNorm(ray_pos, ray_pos - ray_dir);

            float e_tex_val = sampleETex(ray_pos);
            if (e_tex_val != 0.0) ray_hit.light = a_tex_col * e_tex_val * maxLightIntensity;

            break;
        }
    }
    return ray_hit;
}

void main() {
    if (color.w == 0.0) {
        //vec3 nFragPos = round(fragPos * 10.0) / 10.0;
        vec3 norm = normalize(normal);

        vec3 albedo = vec3(0.0);
        for (int i = 0; i < numSamples; i++) {
            vec3 ray_pos = fragPos;
            vec3 ray_norm = norm;
            vec3 ray_albedo = vec3(1.0);
            vec3 ray_light = vec3(0.0);

            for (int j = 0; j < numBounces; j++) {
                vec3 rvec = GetRandomVec3(fragPos + j + i);

                vec3 dir = mix(ray_norm, rvec, 0.49);

                RayHit ray = castRay(dir, ray_pos);

                ray_pos = ray.pos;
                ray_norm = ray.norm;
                ray_albedo *= ray.col;
                
                if (ray.light != vec3(0.0)) {
                    ray_light = ray.light;
                    break;
                }
            }
            albedo += (ray_albedo * ray_light);
        }
        
        albedo /= float(numSamples);

        fragColor = vec4(albedo * color.xyz, 1.0);
    }
    else fragColor = vec4(color.xyz, 1.0);
}