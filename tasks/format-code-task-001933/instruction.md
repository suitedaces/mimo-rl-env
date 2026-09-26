ufuzz failure
```js
// original code
// (beautified)
var _calls_ = 10, a = 100, b = 10, c = 0;

function f0(arguments_1, a_1) {
    {
        var brake1 = 5;
        L12709: while ((c = c + 1) + a++ && --brake1 > 0) {
            try {
            } catch (undefined_2) {
                {
                    var brake4 = 5;
                    do {
                        try {
                            {
                                var brake6 = 5;
                                do {
                                    c = c + 1;
                                } while (/[abc4]/g.exec((typeof undefined_2 !== "object" || b || 5).toString()) && --brake6 > 0);
                            }
                        } catch (arguments_1_1) {
                            c = c + 1;
                            {
                                var await_2 = function f1() {
                                }(25, [ , 0 ][1]);
                            }
                        } finally {
                            class C0 extends (arguments_1 && arguments_1.constructor === Function ? arguments_1 : function() {}) {
                                length(b_2, bar_1) {
                                    {
                                        var expr10 = /[abc4]/g.exec(((c = 1 + c, (true || "a") ^ ("a", -1) && (4 ^ -4) < +38..toString()) || b || 5).toString());
                                        for (a_1 in expr10) {
                                            switch (c = 1 + c, 38..toString() + -2 === 0 % "number" & -(undefined_2 = -4 & -0)) {
                                              case c = 1 + c, (true && 25) & "function" != "a" & (-3 ?? 23..toString()) << (5 != null):
                                                ;
                                                break;

                                              case c = 1 + c, !2 == (Object.isExtensible(bar_1) && (bar_1[c = 1 + c, ("a" + 2 ?? (-1 && /[a2][^e]+$/)) == ((-5 || 2) !== (-4 ^ -3))] = NaN || this)) ^ ~"" == {} > []:
                                                ;
                                                break;

                                              case c = 1 + c, (undefined >= "foo" | (23..toString() || true)) < (Object.isExtensible(a_1) && (a_1.value = NaN % [ , 0 ][1] - (undefined_2 += Infinity && ""))):
                                                ;
                                                break;

                                              case c = 1 + c, Object.isExtensible(bar_1) && (bar_1[(c = c + 1) + {}.var] += (Object.isExtensible(b_2) && (b_2[-3 << -3 != ("a" === -0), 
                                                -3 === "b" == false / "foo"] = !"undefined" >= NaN - "b")) !== (Object.isExtensible(a_1) && (a_1[--b + {}[c = 1 + c, 
                                                null < null > "undefined" / 23..toString() == (+([ , 0 ].length === 2) !== "number" / this)]] %= ("b" >= this) / (1 >> [ , 0 ][1])))):
                                                ;
                                                break;
                                            }
                                        }
                                    }
                                    {
                                        var brake12 = 5;
                                        do {
                                            for (var brake13 = 5; (c = 1 + c, (3 < [] & (this ^ "bar")) >>> ([] >> 4) - ("function" != ([ , 0 ].length === 2))) && brake13 > 0; --brake13) {
                                                c = 1 + c, ((Object.isExtensible(arguments_1) && (arguments_1[c = 1 + c, ("foo" + 2 >= (24..toString() !== this)) / (-0 === ([ , 0 ].length === 2) && 22 ^ null)] = {} + 5)) | (a_1 = 22 && false)) <= (Object.isExtensible(b_2) && (b_2.Infinity = "a" << "b" !== (Object.isExtensible(arguments_1) && (arguments_1[c = 1 + c, 
                                                (c = c + 1, undefined >> [ , 0 ][1]) ^ ([ , 0 ].length === 2) >= 23..toString() & "b" << 24..toString()] += [] + []))));
                                            }
                                        } while ((c = c + 1) + (null === "c" & [ , 0 ][1] * undefined && (-1, -1) % ("foo" % null)) && --brake12 > 0);
                                    }
                                }
                                static #c = (c = c + 1, (/[a2][^e]+$/ === true) << undefined * 1);
                                [(c = c + 1) + a++](foo_2) {
                                    switch ((c = c + 1) + (typeof arguments_1 == "function" && --_calls_ >= 0 && arguments_1(-2))) {
                                      case {
                                            a: (c = 1 + c, ((Object.isExtensible(undefined_2) && (undefined_2.get = "undefined" && "object")) | [] > Number(0xdeadn << 16n | 0xbeefn)) != (2 / "number", 
                                            undefined % 3)),
                                            "\t": (c = 1 + c, (true && undefined) ^ (undefined_2 += -4 < 0) ^ 5 > 38..toString() < null + "foo")
                                        }.set:
                                        break;

                                      case (c = c + 1) + b--:
                                        c = 1 + c, c = c + 1, (-2, [ , 0 ].length === 2) <= ([ , 0 ].length === 2 ?? -4);
                                        c = 1 + c, (undefined_2 = (2 === -0) >>> (24..toString() == "object")) ^ (1 | NaN, 
                                        true === "bar");
                                        break;

                                      default:
                                        c = 1 + c, ({} === "foo") > (c = c + 1, [ , 0 ][1]) | true != "bar" & ("undefined" && -4);

                                      case (c = c + 1) + (b += a):
                                        c = 1 + c, Object.isExtensible(foo_2) && (foo_2[--b + (a_1 && typeof a_1.set == "function" && --_calls_ >= 0 && a_1.set((c = 1 + c, 
                                        (/[a2][^e]+$/ / 38..toString() > (-3 !== 38..toString())) >> ((23..toString() ^ -4) & (a_1 /= 23..toString() ^ "foo"))), 3, -3))] = (38..toString() > -0, 
                                        -2 % []) % (c = c + 1, Infinity - undefined));
                                        c = 1 + c, ("b" << [] ^ (true ^ -0)) & (Object.isExtensible(foo_2) && (foo_2[[]] = (-3 ?? 25) % !1));
                                        break;
                                    }
                                    switch (a++ + [ (c = 1 + c, ((Object.isExtensible(foo_2) && (foo_2[c = 1 + c, (c = c + 1, 
                                    -5) / (-1 == undefined) < (-5 + false !== 24..toString() / 5)] += "bar" == 3)) ^ (Object.isExtensible(foo_2) && (foo_2.async *= -5 <= "c"))) % (2 << "", 
                                    [] === {})), (c = 1 + c, Object.isExtensible(arguments_1) && (arguments_1[!"b" != ("b" === NaN) == (Object.isExtensible(foo_2) && (foo_2.NaN += (4, 
                                    4))) >> ("foo" <= "")] = Object.isExtensible(foo_2) && (foo_2.static &= (-2, [ , 0 ][1]) >>> (38..toString() >= -3)) && ({} | 1) >> (this & -4))), (c = 1 + c, 
                                    (("bar" | -3) ^ (22 && -3)) * ((-3 === this) % ("undefined" > 4))) ].get) {
                                      case --b + (typeof f2 == "function" && --_calls_ >= 0 && f2(25, "number", Infinity)):
                                        break;

                                      case typeof (c = 1 + c, ((Object.isExtensible(undefined_2) && (undefined_2[c = 1 + c, 
                                        Object.isExtensible(undefined_2) && (undefined_2[a++ + undefined_2] &&= ("b" ^ 23..toString()) / (-4 > "foo")) || 38..toString() >> -5 ^ (24..toString() || "number")] &= 22 + false)) == ("", 
                                        0)) / ("function" << ([ , 0 ].length === 2) >= (-4 || "function"))):
                                        c = 1 + c, -0 * 3 < (1 > 22) != "a" >> 25 >= (Infinity !== 2);
                                        c = 1 + c, ~25 !== -3 - "function" | ((undefined_2 = 38..toString() <= undefined) || ([ , 0 ][1], 
                                        4));
                                        break;

                                      case a++ + (b = a):
                                        c = 1 + c, c = c + 1, (-4 ?? "number") <= /[a2][^e]+$/ >>> "object";
                                        break;

                                      case {}.var:
                                        c = 1 + c, ((3 & true) > "bar" * "b") + (/[a2][^e]+$/ != [ , 0 ][1], "undefined" == "c");
                                        break;
                                    }
                                }
                                #get(bar, foo, a_1) {
                                    for (var brake26 = 5; [ (c = 1 + c, (Object.isExtensible(a_1) && (a_1[--b + (a_1 && typeof a_1.value == "function" && --_calls_ >= 0 && a_1.value([], "foo", []))] = true + null !== (25 || 25))) === (undefined == "undefined") >= (-5 < 22)), (c = 1 + c, 
                                    (38..toString() <= 5 <= "object" % true) - ((true == -0) >> ([ , 0 ].length === 2 == -0))) ][c = 1 + c, 
                                    -1 === 3 != "bar" % 38..toString() != (-2 * "" === ([ , 0 ][1] !== 1))] && brake26 > 0; --brake26) {
                                        c = c + 1;
                                    }
                                    var foo = new function bar(bar_2, a_1_1) {
                                        if (this) {
                                            this[c = 1 + c, a_1_1 += (-5 ?? true, 25 ^ "number") >> (38..toString() >= 5) * (undefined >= 24..toString())] += 5 !== [ 3n ][0] > 2;
                                        }
                                        if (this) {
                                            this[c = 1 + c, null - {} >> ("object" & Infinity) ?? ("undefined" ?? -1) ^ /[a2][^e]+$/ / /[a2][^e]+$/] = this << 1;
                                        }
                                    }();
                                }
                                static value = a++ + (typeof a != "symbol");
                            }
                            try {
                                {
                                    var brake30 = 5;
                                    L12710: do {
                                        return;
                                    } while (a++ + (b = a) && --brake30 > 0);
                                }
                            } catch (a_1) {
                                for (var brake32 = 5; (c = 1 + c, undefined_2 && (undefined_2[typeof f2 == "function" && --_calls_ >= 0 && f2((c = 1 + c, 
                                ((a_1 = -3 == "undefined") & (a_1 && (a_1.a += -0 || "foo"))) != ("bar" == 38..toString()) >> (38..toString() || -1)))] += (-5 == /[a2][^e]+$/) >>> (a_1 && (a_1[c = 1 + c, 
                                (2 ^ 1) >>> ("foo" < "foo"), (NaN ^ "function") - (a_1 += [ , 0 ][1] ^ null)] = 0 < undefined)) >>> (false << -2 > ([ , 0 ].length === 2) * null))) && brake32 > 0; --brake32) {
                                    c = 1 + c, 22 > /[a2][^e]+$/ !== true % -3, 22 > 3 == ([ , 0 ][1] ?? -0);
                                }
                                if (c = 1 + c, ([ 3n ][0] > 2) >>> "function" === (-5 != /[a2][^e]+$/) === (3 & -3, 
                                0 >= [ , 0 ][1])) {
                                    c = 1 + c, undefined_2 && (undefined_2.a = (0 & "" | ([ , 0 ].length === 2 | this)) / (-4 !== "c" & ("number" | [ , 0 ][1])));
                                } else {
                                    c = 1 + c, void (-2 | [ , 0 ][1]) && (c = c + 1, 4) ^ 25 !== undefined;
                                }
                            } finally {
                                var b_2;
                                c = c + 1;
                            }
                            switch ((c = c + 1) + +function a_2() {}()) {
                              case --b + (a++ + {
                                    [(c = 1 + c, ("object" <= "object" < ([ , 0 ].length === 2 === 2)) * ("foo" >> NaN ^ (c = c + 1, 
                                    3)))]: (c = 1 + c, 4 != 22 && 38..toString() ** "b", (5 || false) ^ "a" / "undefined"),
                                    get: (c = 1 + c, +(c = c + 1, [] == null))
                                }[c = 1 + c, ([ , 0 ].length === 2 ^ null) === -5 >= 24..toString(), a_1 && (a_1[(c = c + 1) + {
                                    length: (c = 1 + c, "c" === 3 ^ ("a" ?? -2) | (a_1 %= [ , 0 ][1] > 24..toString()) > (undefined | 0))
                                }.get] = (c = c + 1, false) << ("b" < Number(0xdeadn << 16n | 0xbeefn)))] || 9).toString()[void function a_2() {
                                }()]:
                                var b;
                                try {
                                    c = 1 + c, (0 === 3) * (25 + this) & (2, 4) == 1 - false;
                                } catch (yield) {
                                }
                                break;

                              default:
                                {
                                    var expr43 = (c = 1 + c, (arguments_1 && (arguments_1[c = 1 + c, ("c" || [ , 0 ].length === 2, 
                                    this | -5) + (([ , 0 ].length === 2) / "function" == -3 >>> -5)] >>= (Infinity, 
                                    "number"))) != -3 >>> "bar" == ("" % -4 != (23..toString() | false)));
                                    for (var key43 in expr43) {
                                        c = 1 + c;
                                        var arguments_1_2 = expr43[key43];
                                        c = 1 + c, (("number" || "b") >= (0 < "number")) % ((-4 !== 4) >> (undefined_2 && (undefined_2[c = 1 + c, 
                                        (a_1 && (a_1.done = -2 !== [ , 0 ][1] & 24..toString() <= 2)) >>> ("a" >> Infinity < "bar" / "undefined")] += "c" == "function")));
                                    }
                                }

                              case --b + delete a:
                                if (c = 1 + c, (~[] ^ void -0) >> ("function" === "object") / (/[a2][^e]+$/ % 5)) {
                                    c = 1 + c, 22 & "object" ^ "function" < 2 ^ -3 >> ([ , 0 ].length === 2) <= (5 == "undefined");
                                } else {
                                    c = 1 + c, arguments_1 && (arguments_1[--b + ~(2 < 38..toString() <= ("number", 
                                    "number") > (a_1 && (a_1[c = 1 + c, [ , 0 ][1] >> 4 >>> "function" / {} != (25 && 23..toString()) > ("" == "number")] += 24..toString() > 24..toString())) % ("" ^ 4))] = (-5 >> this >= (-5 == [ 3n ][0] > 2)) + (arguments_1 && (arguments_1[--b + /[abc4]/g.exec(((c = 1 + c, 
                                    ({} + -5 || 0 % 4) & (-3 << true && 2 == 22)) || b || 5).toString())] = -5 >>> ([ , 0 ].length === 2) <= (-0 != 22))));
                                }
                                {
                                    return c = 1 + c, ("number" >= 1 < (undefined_2 = 23..toString() != 3)) << (-2 <= 4) % (c = c + 1, 
                                    /[a2][^e]+$/);
                                }
                                break;

                              case ((yield, bar) => typeof arguments_1 == "function" && --_calls_ >= 0 && arguments_1((c = 1 + c, 
                                (/[a2][^e]+$/ * true & ("a" || "bar")) >>> delete (0 ^ 3)), Infinity, (c = 1 + c, 
                                (22 ^ "bar") <= ([ , 0 ][1] & false) < (1 && 22 && /[a2][^e]+$/ >>> "bar"))))():
                            }
                        }
                    } while (a++ + (a_1 = a++ + (arguments_1 && typeof arguments_1.a == "function" && --_calls_ >= 0 && ({
                        async: --b + {
                            a: (c = 1 + c, -(0 >= "number" < (0 !== 23..toString()))),
                            "\t": (c = 1 + c, (2 !== -0 && -3 ^ NaN) >= (24..toString() ^ "number") >> (-2 ?? undefined)),
                            1.5: (c = 1 + c, (-3 === null) - (arguments_1 && (arguments_1[c = 1 + c, ("b" < [ , 0 ][1]) >>> (a_1 && (a_1.null = "a" <= -0)) === (0 || "number") % ("c" == "bar")] /= -2 + -1)) & (undefined_2 && (undefined_2.next = undefined < "c")) > "b" - -5),
                            null: (c = 1 + c, (a_1 && (a_1[a++ + ((c = 1 + c, (0 ?? -3) * (NaN % /[a2][^e]+$/) && -0 / "foo" << (-5 >>> 5)) ? (c = 1 + c, 
                            a_1 && (a_1[1 === 1 ? a : b] = ("c" >>> "foo" < /[a2][^e]+$/ >>> "b") >>> (24..toString() !== "" == "undefined" >= -5))) : (c = 1 + c, 
                            -3 * 5 > (Infinity && /[a2][^e]+$/) != ((38..toString() ^ "number") & 24..toString() == "number")))] **= (c = c + 1, 
                            false) >= ("undefined" !== 38..toString()))) >= (-0 & 22) * ([] == -1)),
                            3: (c = 1 + c, (-4 % 22 == 0 < 23..toString()) < (-5 - "number") / (-0 & "c"))
                        }.done,
                        [(c = c + 1) + a++]: a--
                    }[--b + a--], arguments_1.a)`${a++ + (typeof a_1 == "function" && --_calls_ >= 0 && a_1((c = 1 + c, 
                    "function" & 0 | "function" !== "number" && ([] ^ 3) * (Infinity % undefined)), (c = 1 + c, 
                    (4 < Infinity) - 38..toString() * true >> (undefined_2 && (undefined_2[(c = c + 1) + (undefined_2 && typeof undefined_2.set == "function" && --_calls_ >= 0 && undefined_2.set((c = 1 + c, 
                    (Infinity || null) <= -4 * "c" && 3 % undefined - (-4 | NaN)), (c = 1 + c, a_1 && (a_1[(c = c + 1) + (typeof arguments_1 == "function" && --_calls_ >= 0 && arguments_1((c = 1 + c, 
                    (22 ^ "foo") >= [] << "undefined" !== ("foo" * 25 ^ -1 !== null)), "number"))] += ("bar" ^ [ , 0 ].length === 2 || (c = c + 1, 
                    2)) == (true === "b") <= (3 ^ {})))))] = /[a2][^e]+$/ <= "foo" && Infinity > /[a2][^e]+$/)))))}`)) && --brake4 > 0);
                }
                switch (arguments_1) {
                  default:
                    ;

                  case -((arguments_1 && (arguments_1[c = 1 + c, ("object" !== 5 & (arguments_1 |= "b" == false)) ** ((Infinity ^ 4) + -0 * 23..toString())] ||= false >>> [])) === "object" / 38..toString() ?? -NaN * (a_1 += -2 % true)):
                    {
                        break;
                    }
                    break;

                  case [ (c = c + 1) + (undefined in []), a++ + ((arguments_1 && (arguments_1[c = 1 + c, 
                    (undefined_2 && (undefined_2.Infinity = (2 != -2) << (/[a2][^e]+$/, "number"))) - (-1 << 2 >>> (undefined_2 && (undefined_2.value = "foo" / 24..toString())))] = -0 | "number"), 
                    undefined - 3) | -0 << 0 >= (NaN > 38..toString())), a_1 && a_1[0 in {
                        static: (c = 1 + c, arguments_1 && (arguments_1.undefined += -0 >= 23..toString() & undefined >>> 38..toString() | (3 ^ 4) !== 0 < "a")),
                        b: (c = 1 + c, a_1 && (a_1[~a] = ([ , 0 ][1] ^ Infinity) === 2 > 1), ([ , 0 ].length === 2 & true) === ([] != 4))
                    }] ].value:
                    c = c + 1;
                    break;

                  case a++ + void function await_2() {}():
                    break;
                }
            } finally {
                {
                    var brake55 = 5;
                    do {
                        {
                            var brake56 = 5;
                            while (a_1 && --brake56 > 0) {
                                var foo_1;
                            }
                        }
                    } while ("object" && --brake55 > 0);
                }
                {
                    var brake58 = 5;
                    while (a++ + (foo_1 *= a_1 += --b + (typeof f3 == "function" && --_calls_ >= 0 && f3(+function Infinity_2() {
                    }()))) && --brake58 > 0) {
                        (c = c + 1) + a--;
                    }
                }
            }
        }
    }
    {
        var expr60 = a_1 && typeof a_1.async == "function" && --_calls_ >= 0 && a_1.async(-0, {});
        for (var key60 in expr60) {
            c = 1 + c;
            var foo = expr60[key60];
            try {
                c = c + 1;
            } finally {
                {
                    var foo_1 = function f2() {
                        {
                            try {
                                c = 1 + c, (arguments_1 >>= ("object", -3)) == -5 >> "object" ?? (38..toString() && "b" || "number" >>> 38..toString());
                            } finally {
                            }
                        }
                        if ([ (c = 1 + c, undefined ^ "number" ^ ([ , 0 ][1] ^ false), (undefined === -2) / (25 * 24..toString())), (c = 1 + c, 
                        ("undefined" - "") * (38..toString() >> -4) >>> 0 / 3 - ("a" !== "undefined")), (c = 1 + c, 
                        a_1 = (-3 << [], null / undefined) ^ "c" * "foo" >> (Infinity ^ undefined)), (c = 1 + c, 
                        delete ("a" <= -1) === (null - 1 !== ([ , 0 ][1] ^ [ , 0 ][1]))) ][(c = c + 1) + (a_1 && a_1.NaN)]) {
                            var arguments = function yield() {
                            }();
                        }
                    }(false, a++ + (-5 in [ --b + (b &= a) ]), "bar");
                }
                var a_2 = a++ + ([ typeof foo == "function" && --_calls_ >= 0 && foo(23..toString(), (c = 1 + c, 
                (a_2 && ({
                    async: a_2[(c = c + 1) + ((c = 1 + c, (arguments_1 && ({
                        3: arguments_1[c = 1 + c, (false ^ {}) >> 25 / [] && (-0 || "a") * ("foo" < this)]
                    } = {
                        3: 3 >> [ , 0 ][1]
                    })) >> (([ , 0 ].length === 2) <= "b") << ("a" < "function") % ("" != 2)) || a || 3).toString()]
                } = {
                    async: "" > 1 === 1 << -3
                })) === (a_1 && (a_1[(c = c + 1) + ((c = 1 + c, (0 & "undefined") * (3 <= -2) !== (38..toString() == 24..toString()) + -2 * "") || 6).toString()[c = 1 + c, 
                /[a2][^e]+$/ * /[a2][^e]+$/ + (-5 || []) > (([] !== !0o644n) > /[a2][^e]+$/ << 1)]] = ("object" <= 25) / (-4 % ([ , 0 ].length === 2))))), 0), (c = c + 1) + (key60 += (c = c + 1) + void +(({} | 23..toString()) == (1 == "number"))), (c = c + 1) + {}.Infinity, {
                    set: (c = 1 + c, ((NaN, null) <= ({} > 24..toString())) << (foo && (foo[c = 1 + c, 
                    (this != "undefined" && "object" * NaN) < ((this == [ 3n ][0] > 2) >= (-0 === 3))] %= this !== undefined) && 4 ^ 3)),
                    static: (c = 1 + c, (foo_1 /= ("number" >= this) / (38..toString() >> 0)) <= ((c = c + 1, 
                    4) > true - [ , 0 ][1]))
                }, --b + (a_2 && a_2[~a]) ][void function() {
                    c = 1 + c, ("object" != -5) << 24..toString() / -5 ^ ("c" & null) / (-5 != undefined);
                    c = 1 + c, (c = c + 1, 1 !== Infinity) % (/[a2][^e]+$/ * null && ({} && undefined));
                }() ? foo && foo[--b] : (c = c + 1) + a++] ? a++ + (a_1 && a_1.a) : a--), foo_1 = (c = c + 1) + (foo_1 && foo_1.async);
            }
        }
    }
}

var NaN_2 = f0(typeof f3 == "function" && --_calls_ >= 0 && f3(..."" + NaN_2, typeof NaN_2 == "function" && --_calls_ >= 0 && NaN_2()));

console.log(null, a, b, c, Infinity, NaN, undefined);
```
```js
// uglified code
// (beautified)
var _calls_ = 10, a = 100, b = 10, c = 0;

function f0(arguments_1, a_1) {
    for (var b, brake1 = 5; (c += 1) + a++ && 0 < --brake1; ) {
        (class extends (arguments_1 && arguments_1.constructor === Function ? arguments_1 : function() {}) {
            [(c += 1, a++)]() {}
        }), (() => (c += 1, a++))();
        var brake55 = 5;
        do {
            for (var brake56 = 5; a_1 && 0 < --brake56; ) {}
        } while (0 < --brake55);
        for (var brake58 = 5; a++ + (foo_1 *= a_1 += --b + ("function" == typeof f3 && 0 <= --_calls_ && f3(NaN))) && 0 < --brake58; ) {
            c += 1, a--;
        }
    }
    var key60, expr60 = a_1 && "function" == typeof a_1.async && 0 <= --_calls_ && a_1.async(-0, {});
    for (key60 in expr60) {
        c = 1 + c;
        var foo = expr60[key60];
        try {
            c += 1;
        } finally {
            var foo_1 = function() {
                c = 1 + c, -5 == (arguments_1 >>= -3) ?? (38..toString() || 38..toString()), c = 1 + c, 
                24..toString(), c = 1 + c, 38..toString(), a_1 = 0, c = 1 + (c = 1 + c), c += 1, 
                a_1 && a_1.NaN;
            }(!1, a++ + (-5 in [ --b + (b &= a) ]), "bar"), a_2 = a++ + ([ "function" == typeof foo && 0 <= --_calls_ && foo(23..toString(), (c = 1 + c, 
            (a_2 && ({
                async: a_2[(c += 1) + (c = 1 + c, ((arguments_1 && ({
                    3: arguments_1[c = 1 + c, (!1 ^ {}) >> 25 / [] && "a" * ("foo" < this)]
                } = {
                    3: 3
                })) >> ((2 === [ , 0 ].length) <= "b") << 0 || a || 3).toString())]
            } = {
                async: !1
            })) === (a_1 && (a_1[(c += 1) + (c = 1 + c, (0 != (38..toString() == 24..toString()) + -0 || 6).toString()[c = 1 + c, 
            0 < (!0o644n !== []) < NaN])] = !1 / (-4 % (2 === [ , 0 ].length))))), 0), (c += 1) + (key60 += (c += 1) + void 23..toString()), (c += 1) + {}.Infinity, {
                set: (c = 1 + c, (null <= ({} > 24..toString())) << (foo && (foo[c = 1 + c, ("undefined" != this && NaN) < (!1 <= (this == 2 < 3n))] %= void 0 !== this) && 7)),
                static: (c = 1 + c, (foo_1 /= (this <= "number") / (38..toString() >> 0)) <= (c += 1, 
                !0))
            }, --b + (a_2 && a_2[~a]) ][c = 1 + c, 24..toString(), c = 1 + c, c += 1, (c += 1) + a++] ? a++ + (a_1 && a_1.a) : a--), foo_1 = (c += 1) + (foo_1 && foo_1.async);
        }
    }
}

var NaN_2 = f0("function" == typeof f3 && 0 <= --_calls_ && f3(..."" + NaN_2, "function" == typeof NaN_2 && 0 <= --_calls_ && NaN_2()));

console.log(null, a, b, c, 1 / 0, NaN, void 0);
```
```
original result:
null 109 10 5 Infinity NaN undefined

uglified result:
null 117 10 13 Infinity NaN undefined
```
```js
// reduced test case (output will differ)

// (beautified)
try {} catch (undefined_2) {
    class C0 extends 0 {}
}
// output: 
// minify: TypeError: Class extends value 0 is not a constructor or null
// options: {
//   "mangle": false,
//   "output": {
//     "v8": true
//   },
//   "validate": true
// }
```
```
minify(options):
{
  "mangle": false,
  "output": {
    "v8": true
  }
}

Suspicious compress options:
  dead_code
```
