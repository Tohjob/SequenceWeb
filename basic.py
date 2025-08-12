from flask import Flask, render_template, request
import math

app = Flask(__name__)

def fmt(x):
    if x is None:
        return "ไม่สามารถคำนวณได้"
    if abs(x - round(x)) < 1e-12:
        return str(int(round(x)))
    return f"{x:.6g}"

def general_formula(a1, dr, stype):
    if stype == "arithmetic":
        return f"aₙ = {fmt(a1)} + (n - 1) × {fmt(dr)}"
    else:
        return f"aₙ = {fmt(a1)} × ({fmt(dr)})^(n - 1)"

def compute_an(a1, dr, n, stype):
    if stype == "arithmetic":
        return a1 + (n - 1) * dr
    else:
        return a1 * (dr ** (n - 1))

def sum_sn(a1, dr, n, stype):
    if stype == "arithmetic":
        return (n / 2) * (2 * a1 + (n - 1) * dr)
    else:
        r = dr
        if abs(r - 1) < 1e-12:
            return a1 * n
        return a1 * (1 - r ** n) / (1 - r)

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    error = None
    data = {
        "seq_type": "arithmetic",
        "operation": "รูปทั่วไป (General formula)",
        "a1": "",
        "dr": "",
        "n": "",
        "ak": "",
        "k": "",
        "am": "",
        "m": "",
        "an": "",
    }

    if request.method == "POST":
        # อ่านข้อมูลจากฟอร์ม
        data["seq_type"] = request.form.get("seq_type", "arithmetic")
        data["operation"] = request.form.get("operation", "รูปทั่วไป (General formula)")
        data["a1"] = request.form.get("a1", "").strip()
        data["dr"] = request.form.get("dr", "").strip()
        data["n"] = request.form.get("n", "").strip()
        data["ak"] = request.form.get("ak", "").strip()
        data["k"] = request.form.get("k", "").strip()
        data["am"] = request.form.get("am", "").strip()
        data["m"] = request.form.get("m", "").strip()
        data["an"] = request.form.get("an", "").strip()

        # แปลงข้อมูล
        def to_float(s):
            try:
                return float(s)
            except:
                return None

        def to_int(s):
            try:
                return int(float(s))
            except:
                return None

        stype = data["seq_type"]
        op = data["operation"]

        a1 = to_float(data["a1"])
        dr = to_float(data["dr"])
        n = to_int(data["n"])
        ak = to_float(data["ak"])
        am = to_float(data["am"])
        k = to_int(data["k"])
        m = to_int(data["m"])
        an = to_float(data["an"])

        try:
            if op.startswith("รูปทั่วไป"):
                if a1 is None or dr is None:
                    error = "กรุณากรอก a1 และ d หรือ r ให้ถูกต้อง"
                else:
                    result.append("รูปทั่วไป:")
                    result.append(general_formula(a1, dr, stype))

            elif op.startswith("หา aₙ"):
                if a1 is None or dr is None or n is None or n <= 0:
                    error = "กรุณากรอก a1, d/r และ n (จำนวนเต็มบวก) ให้ถูกต้อง"
                else:
                    an_res = compute_an(a1, dr, n, stype)
                    result.append(general_formula(a1, dr, stype))
                    result.append(f"a{n} = {fmt(an_res)}")

            elif op.startswith("หา n"):
                if a1 is None or dr is None or an is None:
                    error = "กรุณากรอก a1, d/r และ aₙ ให้ถูกต้อง"
                else:
                    if stype == "arithmetic":
                        if dr == 0:
                            error = "d ต้องไม่เท่ากับ 0"
                        else:
                            n_res = ((an - a1) / dr) + 1
                    else:
                        if dr == 0 or a1 == 0:
                            error = "a1 และ r ต้องไม่เท่ากับ 0"
                        elif an == 0:
                            error = "aₙ ต้องไม่เท่ากับ 0"
                        else:
                            n_res = math.log(an / a1, dr) + 1
                    if error is None:
                        if n_res < 1 or abs(n_res - round(n_res)) > 1e-6:
                            result.append(f"ค่า n ที่คำนวณได้: {n_res:.6f} (ไม่ใช่จำนวนเต็มบวก)")
                        else:
                            n_int = round(n_res)
                            result.append(general_formula(a1, dr, stype))
                            result.append(f"aₙ = {fmt(an)}")
                            result.append(f"พจน์ที่ n = {fmt(n_int)}")

            elif op.startswith("หา d") or op.startswith("Find d"):
                if ak is None or am is None or k is None or m is None or k <= 0 or m <= 0 or k == m:
                    error = "กรุณากรอก a_k, a_m และตำแหน่ง k, m ที่เป็นจำนวนเต็มบวก และ k ≠ m"
                else:
                    if stype == "arithmetic":
                        d_res = (am - ak) / (m - k)
                        a1_res = ak - (k - 1) * d_res
                        result.append("ผลลัพธ์ (เลขคณิต):")
                        result.append(f"d = (a{m} - a{k}) / ({m} - {k}) = {fmt(d_res)}")
                        result.append(f"a1 = a{k} - (k-1)d = {fmt(a1_res)}")
                        result.append(f"รูปทั่วไป: aₙ = {fmt(a1_res)} + (n-1)×{fmt(d_res)}")
                    else:
                        if ak == 0 or am == 0:
                            error = "a_k หรือ a_m = 0 ไม่สามารถหา r ได้ (หารด้วย 0)"
                        else:
                            ratio = am / ak
                            power = 1.0 / (m - k)
                            r_res = math.copysign(abs(ratio) ** power, ratio) if ratio < 0 else ratio ** power
                            a1_res = ak / (r_res ** (k - 1))
                            result.append("ผลลัพธ์ (เรขาคณิต):")
                            result.append(f"r = (a{m} / a{k})^(1/({m} - {k})) = {fmt(r_res)}")
                            result.append(f"a1 = a{k} / r^({k-1}) = {fmt(a1_res)}")
                            result.append(f"รูปทั่วไป: aₙ = {fmt(a1_res)} × ({fmt(r_res)})^(n-1)")

            elif op.startswith("ผลรวม"):
                if a1 is None or dr is None or n is None or n <= 0:
                    error = "กรุณากรอก a1, d/r และ n (จำนวนเต็มบวก) ให้ถูกต้อง"
                else:
                    sn_res = sum_sn(a1, dr, n, stype)
                    result.append(f"ผลรวม Sₙ:")
                    result.append(f"S{n} = {fmt(sn_res)}")
                    if stype == "arithmetic":
                        result.append("สูตร (เลขคณิต): Sₙ = n/2 × (2a₁ + (n-1)d)")
                    else:
                        result.append("สูตร (เรขาคณิต): Sₙ = a₁(1 - r^n)/(1 - r)  (ถ้า r ≠ 1)")
            else:
                error = "เลือกการทำงานไม่ถูกต้อง"

        except Exception as e:
            error = f"เกิดข้อผิดพลาด: {e}"

    return render_template("index.html", data=data, result=result, error=error)


if __name__ == "__main__":
       import os 
       port = int(os.environ.get("PORT", 8080))
       app.run(host="0.0.0.0", port=port)