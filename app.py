from flask import Flask, request, render_template_string
import joblib
import os # <-- Thêm thư viện os

# --- PHẦN CẬP NHẬT ---
# Lấy đường dẫn thư mục hiện tại của file app.py
base_dir = os.path.dirname(os.path.abspath(__file__))
# Tạo đường dẫn an toàn đến file model
model_path = os.path.join(base_dir, 'main_model.pkl')

app = Flask(__name__)
# Load model bằng đường dẫn an toàn
model = joblib.load(model_path)
# --- KẾT THÚC CẬP NHẬT ---


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi" data-bs-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dự đoán nguy cơ thai sản</title>

  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"/>

  <style>
    :root{
      --brand:#6750f0;
      --brand-2:#8e7bff;
      --bg:#0f172a;
      --border:rgba(255,255,255,0.14);
      --text:#e5e7eb;
      --muted:#9ca3af;
      --low-bg:#0b3b2a;  --low-chip:#22c55e;
      --mid-bg:#2a2307;  --mid-chip:#fbbf24;
      --high-bg:#3a0f16; --high-chip:#f43f5e;
    }
    body{
      background: radial-gradient(1200px 600px at 10% -10%, rgba(142,123,255,.15), transparent 40%),
                  radial-gradient(1200px 600px at 90% 0%, rgba(103,80,240,.15), transparent 40%),
                  var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 30px 12px;
    }
    .app{
      width:100%; max-width:850px;
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(12px);
      border:1px solid var(--border);
      border-radius:20px;
      box-shadow:0 30px 80px rgba(0,0,0,.4);
      overflow:hidden;
      animation:fadeIn .4s ease-out;
    }
    @keyframes fadeIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}

    .app-header{
      background:linear-gradient(135deg,var(--brand),var(--brand-2));
      text-align:center;
      color:#fff;
      padding:24px;
    }
    .app-header h3{margin:0;font-weight:700;}

    .app-body{padding:32px;}
    .field-label{font-weight:600;}
    .input-group-text{background:rgba(255,255,255,0.06);border:1px solid var(--border);color:var(--muted);}
    .form-control{
      background:rgba(255,255,255,0.06);
      border:1px solid var(--border);
      color:var(--text);
    }
    .form-control::placeholder{color:#9ca3af;}
    .form-control:focus{
      background:rgba(255,255,255,0.1);
      border-color:rgba(142,123,255,.6);
      box-shadow:0 0 0 .2rem rgba(142,123,255,.15);
      color:var(--text);
    }

    .btn-primary{
      background:linear-gradient(135deg,var(--brand),var(--brand-2));
      border:none;
      font-weight:700;
      box-shadow:0 8px 30px rgba(103,80,240,.35);
    }
    .btn-primary:hover{filter:brightness(1.07);}
    .btn-outline-secondary{
      color:var(--text);border-color:var(--border);
    }
    .btn-outline-secondary:hover{background:rgba(255,255,255,0.08);}

    .soft-divider{height:1px;background:var(--border);margin:1.25rem 0 1.5rem;}

    .result{
      border-radius:16px;padding:20px 22px;
      border:1px solid var(--border);
      animation:slideIn .3s ease-out;
    }
    @keyframes slideIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}
    .low{background:var(--low-bg);}
    .mid{background:var(--mid-bg);}
    .high{background:var(--high-bg);}
    .chip{
      display:inline-block;
      border-radius:999px;
      padding:8px 16px;
      font-weight:700;
      color:#fff;
    }
    .chip.low{background:var(--low-chip);}
    .chip.mid{background:var(--mid-chip);}
    .chip.high{background:var(--high-chip);}

    .foot{text-align:center;padding:12px;color:var(--muted);font-size:.9rem;border-top:1px solid var(--border);}
  </style>
</head>
<body>
  <div class="app">
    <div class="app-header">
      <h3>Dự đoán nguy cơ thai sản</h3>
    </div>

    <div class="app-body">
      {% if is_post and error_msg %}
        <div class="alert alert-warning mb-3 py-2">{{ error_msg }}</div>
      {% endif %}

      <form method="POST" class="row g-3" novalidate>
        <div class="col-md-6">
  	  <label class="form-label field-label">Tuổi</label>
  	  <div class="input-group">
  		<input type="number" name="age" min="10" max="60" required placeholder="VD: 28" class="form-control" value="{{ request.form.age }}">
  		<span class="input-group-text">tuổi</span>
  	  </div>
  	</div>

  	<div class="col-md-6">
  	  <label class="form-label field-label">Đường huyết</label>
  	  <div class="input-group">
  		<input type="number" name="bs" step="0.1" min="3" max="25" required placeholder="VD: 7.2" class="form-control" value="{{ request.form.bs }}">
  		<span class="input-group-text">mmol/L</span>
  	  </div>
  	</div>

  	<div class="col-md-6">
  	  <label class="form-label field-label">Huyết áp tâm thu</label>
  	  <div class="input-group">
  		<input type="number" name="systolic_bp" step="0.1" min="70" max="250" required placeholder="VD: 120" class="form-control" value="{{ request.form.systolic_bp }}">
  		<span class="input-group-text">mmHg</span>
  	  </div>
  	</div>

  	<div class="col-md-6">
  	  <label class="form-label field-label">Huyết áp tâm trương</label>
  	  <div class="input-group">
  		<input type="number" name="diastolic_bp" step="0.1" min="40" max="150" required placeholder="VD: 80" class="form-control" value="{{ request.form.diastolic_bp }}">
  		<span class="input-group-text">mmHg</span>
  	  </div>
  	</div>

  	<div class="col-md-6">
  	  <label class="form-label field-label">Nhịp tim</label>
  	  <div class="input-group">
  		<input type="number" name="heart_rate" min="40" max="220" required placeholder="VD: 75" class="form-control" value="{{ request.form.heart_rate }}">
  		<span class="input-group-text">bpm</span>
  	  </div>
  	</div>

        <div class="col-12 d-flex gap-2 mt-2">
          <button type="submit" class="btn btn-primary px-4">Dự đoán</button>
          <button type="reset" class="btn btn-outline-secondary">Xóa</button>
        </div>
      </form>

      {% if show_result %}
        <div class="soft-divider"></div>
        <div class="result {{ risk_class }} text-center">
          <span class="chip {{ risk_class }}">{{ result }}</span>
        </div>
      {% endif %}
    </div>

    <div class="foot">CT312 - Khai khoáng dữ liệu - Đề tài 09</div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def predict():
    result = None
    risk_class = None
    error_msg = None
    show_result = False
    is_post = (request.method == "POST")

    if is_post:
        # Chỉ xử lý khi form có đầy đủ key
        required_keys = ("age", "systolic_bp", "diastolic_bp", "bs", "heart_rate")
        form = request.form

        missing = [k for k in required_keys if not form.get(k)]
        if missing:
            # Người dùng đã submit nhưng thiếu dữ liệu
            error_msg = "Dữ liệu không hợp lệ. Vui lòng nhập lại."
        else:
            try:
                age = float(form.get("age", "").strip())
                systolic_bp = float(form.get("systolic_bp", "").strip())
                diastolic_bp = float(form.get("diastolic_bp", "").strip())
                bs = float(form.get("bs", "").strip())
                heart_rate = float(form.get("heart_rate", "").strip())

                # Tính MAP
                map_value = diastolic_bp + (systolic_bp - diastolic_bp) / 3.0

                # Dự đoán
                prediction = model.predict([[age, bs, heart_rate, map_value]])[0]

                mapping = {
                    0: ("Nguy cơ thấp", "low"),
                    1: ("Nguy cơ trung bình", "mid"),
                    2: ("Nguy cơ cao", "high"),
                }

                if int(prediction) in mapping:
                    result, risk_class = mapping[int(prediction)]
                    show_result = True
                else:
                    error_msg = "Kết quả không xác định từ mô hình."
            except ValueError:
                # Lỗi chuyển kiểu số (nhập sai định dạng)
                error_msg = "Dữ liệu không hợp lệ. Vui lòng nhập lại."
            except Exception:
                # Lỗi không mong muốn khác
                error_msg = "Đã xảy ra lỗi khi dự đoán. Vui lòng thử lại."

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        risk_class=risk_class,
        error_msg=error_msg,
        show_result=show_result,
  	is_post=is_post,
  	request=request # <-- Truyền biến request vào template
    )

if __name__ == "__main__":
    # Chạy Flask
    app.run(debug=True)
