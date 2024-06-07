import execjs

key = "k8tUyS$m"
ctx = execjs.compile(
        """
var Br = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof global < "u" ? global : typeof self < "u" ? self : {};
var xy = {
    exports: {}
};
var rf = {
    exports: {}
}, Pg;
function vq() {
    return Pg || (Pg = 1,
    function(e, t) {
        (function(n, u) {
            e.exports = u()
        }
        )(Br, function() {
            var n = n || function(u, o) {
                var r;
                if (typeof window < "u" && window.crypto && (r = window.crypto),
                typeof self < "u" && self.crypto && (r = self.crypto),
                typeof globalThis < "u" && globalThis.crypto && (r = globalThis.crypto),
                !r && typeof window < "u" && window.msCrypto && (r = window.msCrypto),
                !r && typeof Br < "u" && Br.crypto && (r = Br.crypto),
                !r && typeof Eq == "function")
                    try {
                        r = YC
                    } catch(err) {}
                var i = function() {
                    if (r) {
                        if (typeof r.getRandomValues == "function")
                            try {
                                return r.getRandomValues(new Uint32Array(1))[0]
                            } catch(err) {}
                        if (typeof r.randomBytes == "function")
                            try {
                                return r.randomBytes(4).readInt32LE()
                            } catch(err) {}
                    }
                    throw new Error("Native crypto module could not be used to get secure random number.")
                }
                  , s = Object.create || function() {
                    function C() {}
                    return function(B) {
                        var x;
                        return C.prototype = B,
                        x = new C,
                        C.prototype = null,
                        x
                    }
                }()
                  , a = {}
                  , l = a.lib = {}
                  , c = l.Base = function() {
                    return {
                        extend: function(C) {
                            var B = s(this);
                            return C && B.mixIn(C),
                            (!B.hasOwnProperty("init") || this.init === B.init) && (B.init = function() {
                                B.$super.init.apply(this, arguments)
                            }
                            ),
                            B.init.prototype = B,
                            B.$super = this,
                            B
                        },
                        create: function() {
                            var C = this.extend();
                            return C.init.apply(C, arguments),
                            C
                        },
                        init: function() {},
                        mixIn: function(C) {
                            for (var B in C)
                                C.hasOwnProperty(B) && (this[B] = C[B]);
                            C.hasOwnProperty("toString") && (this.toString = C.toString)
                        },
                        clone: function() {
                            return this.init.prototype.extend(this)
                        }
                    }
                }()
                  , f = l.WordArray = c.extend({
                    init: function(C, B) {
                        C = this.words = C || [],
                        B != o ? this.sigBytes = B : this.sigBytes = C.length * 4
                    },
                    toString: function(C) {
                        return (C || h).stringify(this)
                    },
                    concat: function(C) {
                        var B = this.words
                          , x = C.words
                          , b = this.sigBytes
                          , _ = C.sigBytes;
                        if (this.clamp(),
                        b % 4)
                            for (var D = 0; D < _; D++) {
                                var I = x[D >>> 2] >>> 24 - D % 4 * 8 & 255;
                                B[b + D >>> 2] |= I << 24 - (b + D) % 4 * 8
                            }
                        else
                            for (var O = 0; O < _; O += 4)
                                B[b + O >>> 2] = x[O >>> 2];
                        return this.sigBytes += _,
                        this
                    },
                    clamp: function() {
                        var C = this.words
                          , B = this.sigBytes;
                        C[B >>> 2] &= 4294967295 << 32 - B % 4 * 8,
                        C.length = u.ceil(B / 4)
                    },
                    clone: function() {
                        var C = c.clone.call(this);
                        return C.words = this.words.slice(0),
                        C
                    },
                    random: function(C) {
                        for (var B = [], x = 0; x < C; x += 4)
                            B.push(i());
                        return new f.init(B,C)
                    }
                })
                  , d = a.enc = {}
                  , h = d.Hex = {
                    stringify: function(C) {
                        for (var B = C.words, x = C.sigBytes, b = [], _ = 0; _ < x; _++) {
                            var D = B[_ >>> 2] >>> 24 - _ % 4 * 8 & 255;
                            b.push((D >>> 4).toString(16)),
                            b.push((D & 15).toString(16))
                        }
                        return b.join("")
                    },
                    parse: function(C) {
                        for (var B = C.length, x = [], b = 0; b < B; b += 2)
                            x[b >>> 3] |= parseInt(C.substr(b, 2), 16) << 24 - b % 8 * 4;
                        return new f.init(x,B / 2)
                    }
                }
                  , p = d.Latin1 = {
                    stringify: function(C) {
                        for (var B = C.words, x = C.sigBytes, b = [], _ = 0; _ < x; _++) {
                            var D = B[_ >>> 2] >>> 24 - _ % 4 * 8 & 255;
                            b.push(String.fromCharCode(D))
                        }
                        return b.join("")
                    },
                    parse: function(C) {
                        for (var B = C.length, x = [], b = 0; b < B; b++)
                            x[b >>> 2] |= (C.charCodeAt(b) & 255) << 24 - b % 4 * 8;
                        return new f.init(x,B)
                    }
                }
                  , m = d.Utf8 = {
                    stringify: function(C) {
                        try {
                            return decodeURIComponent(escape(p.stringify(C)))
                        } catch(err) {
                            throw new Error("Malformed UTF-8 data")
                        }
                    },
                    parse: function(C) {
                        return p.parse(unescape(encodeURIComponent(C)))
                    }
                }
                  , v = l.BufferedBlockAlgorithm = c.extend({
                    reset: function() {
                        this._data = new f.init,
                        this._nDataBytes = 0
                    },
                    _append: function(C) {
                        typeof C == "string" && (C = m.parse(C)),
                        this._data.concat(C),
                        this._nDataBytes += C.sigBytes
                    },
                    _process: function(C) {
                        var B, x = this._data, b = x.words, _ = x.sigBytes, D = this.blockSize, I = D * 4, O = _ / I;
                        C ? O = u.ceil(O) : O = u.max((O | 0) - this._minBufferSize, 0);
                        var P = O * D
                          , j = u.min(P * 4, _);
                        if (P) {
                            for (var H = 0; H < P; H += D)
                                this._doProcessBlock(b, H);
                            B = b.splice(0, P),
                            x.sigBytes -= j
                        }
                        return new f.init(B,j)
                    },
                    clone: function() {
                        var C = c.clone.call(this);
                        return C._data = this._data.clone(),
                        C
                    },
                    _minBufferSize: 0
                });
                l.Hasher = v.extend({
                    cfg: c.extend(),
                    init: function(C) {
                        this.cfg = this.cfg.extend(C),
                        this.reset()
                    },
                    reset: function() {
                        v.reset.call(this),
                        this._doReset()
                    },
                    update: function(C) {
                        return this._append(C),
                        this._process(),
                        this
                    },
                    finalize: function(C) {
                        C && this._append(C);
                        var B = this._doFinalize();
                        return B
                    },
                    blockSize: 16,
                    _createHelper: function(C) {
                        return function(B, x) {
                            return new C.init(x).finalize(B)
                        }
                    },
                    _createHmacHelper: function(C) {
                        return function(B, x) {
                            return new g.HMAC.init(C,x).finalize(B)
                        }
                    }
                });
                var g = a.algo = {};
                return a
            }(Math);
            return n
        })
    }(rf)),
    rf.exports
}
// 匿名函数
(function(e, t) {
    (function(n, u) {
        e.exports = u(vq())
    }
    )(Br, function(n) {
        return function(u) {
            var o = n
              , r = o.lib
              , i = r.WordArray
              , s = r.Hasher
              , a = o.algo
              , l = []
              , c = [];
            (function() {
                function h(g) {
                    for (var C = u.sqrt(g), B = 2; B <= C; B++)
                        if (!(g % B))
                            return !1;
                    return !0
                }
                function p(g) {
                    return (g - (g | 0)) * 4294967296 | 0
                }
                for (var m = 2, v = 0; v < 64; )
                    h(m) && (v < 8 && (l[v] = p(u.pow(m, 1 / 2))),
                    c[v] = p(u.pow(m, 1 / 3)),
                    v++),
                    m++
            }
            )();
            var f = []
              , d = a.SHA256 = s.extend({
                _doReset: function() {
                    this._hash = new i.init(l.slice(0))
                },
                _doProcessBlock: function(h, p) {
                    for (var m = this._hash.words, v = m[0], g = m[1], C = m[2], B = m[3], x = m[4], b = m[5], _ = m[6], D = m[7], I = 0; I < 64; I++) {
                        if (I < 16)
                            f[I] = h[p + I] | 0;
                        else {
                            var O = f[I - 15]
                              , P = (O << 25 | O >>> 7) ^ (O << 14 | O >>> 18) ^ O >>> 3
                              , j = f[I - 2]
                              , H = (j << 15 | j >>> 17) ^ (j << 13 | j >>> 19) ^ j >>> 10;
                            f[I] = P + f[I - 7] + H + f[I - 16]
                        }
                        var Y = x & b ^ ~x & _
                          , L = v & g ^ v & C ^ g & C
                          , M = (v << 30 | v >>> 2) ^ (v << 19 | v >>> 13) ^ (v << 10 | v >>> 22)
                          , U = (x << 26 | x >>> 6) ^ (x << 21 | x >>> 11) ^ (x << 7 | x >>> 25)
                          , R = D + U + Y + c[I] + f[I]
                          , ee = M + L;
                        D = _,
                        _ = b,
                        b = x,
                        x = B + R | 0,
                        B = C,
                        C = g,
                        g = v,
                        v = R + ee | 0
                    }
                    m[0] = m[0] + v | 0,
                    m[1] = m[1] + g | 0,
                    m[2] = m[2] + C | 0,
                    m[3] = m[3] + B | 0,
                    m[4] = m[4] + x | 0,
                    m[5] = m[5] + b | 0,
                    m[6] = m[6] + _ | 0,
                    m[7] = m[7] + D | 0
                },
                _doFinalize: function() {
                    var h = this._data
                      , p = h.words
                      , m = this._nDataBytes * 8
                      , v = h.sigBytes * 8;
                    return p[v >>> 5] |= 128 << 24 - v % 32,
                    p[(v + 64 >>> 9 << 4) + 14] = u.floor(m / 4294967296),
                    p[(v + 64 >>> 9 << 4) + 15] = m,
                    h.sigBytes = p.length * 4,
                    this._process(),
                    this._hash
                },
                clone: function() {
                    var h = s.clone.call(this);
                    return h._hash = this._hash.clone(),
                    h
                }
            });
            o.SHA256 = s._createHelper(d),
            o.HmacSHA256 = s._createHmacHelper(d)
        }(Math),
        n.SHA256
    })
}
)(xy);
var Cq = xy.exports;

// var k="k8tUyS$m",n="XgsNo3npVzcW9DOU",p="",t=1676974388321, r = Bq(t);
// const {p: t, t: n, n: u, k: o} = e
//      , r = Bq(t);
//    return Cq(u + o + decodeURIComponent(r) + n)

function Bq(e) {
    let t = "";
    return typeof e == "object" ? t = Object.keys(e).map(n=>`${n}=${e[n]}`).sort().join("&") : typeof e == "string" && (t = e.split("&").sort().join("&")),
    t
}
function Ig(params) {
    // k8tUyS$m
    //var r = Bq(t);
    //var C = Cq(a+c+decodeURIComponent(r)+l)
    var C = Cq(params)
    for (var B = C.words, x = C.sigBytes, b = [], _ = 0; _ < x; _++) {
                var D = B[_ >>> 2] >>> 24 - _ % 4 * 8 & 255;
                b.push((D >>> 4).toString(16)),
                b.push((D & 15).toString(16))
            }
    return b.join("")
}
        """
)