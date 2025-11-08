from flask import Flask, request, render_template_string, redirect, url_for, session
import joblib

app = Flask(__name__)
app.secret_key = 'de_tai_09' 
model = joblib.load('main_model.pkl')

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
      --brand:#1e40af;
      --brand-2:#3b82f6;
      --bg:#f8fafc;
      --border:rgba(30,64,175,0.15);
      --text:#1e293b;
      --muted:#64748b;
      --low-bg:#ecfdf5;  --low-chip:#10b981;
      --mid-bg:#fef3c7;  --mid-chip:#f59e0b;
      --high-bg:#fee2e2; --high-chip:#ef4444;
    }
    body{
      background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 50%, #e0e7ff 100%);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 30px 12px;
    }
    .app{
      width:100%; max-width:1200px;
      background: #ffffff;
      backdrop-filter: blur(12px);
      border:1px solid var(--border);
      border-radius:20px;
      box-shadow:0 20px 60px rgba(30,64,175,.12);
      overflow:hidden;
      animation:fadeIn .4s ease-out;
    }
    @keyframes fadeIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}

    .main-layout{
      display:grid;
      grid-template-columns:280px 1fr 280px;
      gap:0;
    }
    @media (max-width: 1024px){
      .main-layout{
        grid-template-columns:1fr;
      }
      .left-sidebar, .right-sidebar{
        display:none;
      }
    }

    .app-header{
      background:linear-gradient(135deg,var(--brand),var(--brand-2));
      text-align:center;
      color:#fff;
      padding:24px;
    }
    .app-header h3{margin:0;font-weight:700;}

    .left-sidebar, .right-sidebar{
      background:#f1f5f9;
      padding:28px 22px;
      border-right:1px solid var(--border);
    }
    .right-sidebar{
      border-right:none;
      border-left:1px solid var(--border);
    }
    .sidebar-title{
      color:var(--brand);
      font-size:1rem;
      font-weight:700;
      margin:0 0 18px 0;
      display:flex;
      align-items:center;
      gap:8px;
      padding-bottom:14px;
      border-bottom:2px solid rgba(59,130,246,0.3);
    }
    .info-item{
      margin-bottom:14px;
      font-size:0.85rem;
      line-height:1.5;
      color:var(--text);
    }
    .info-item:last-child{
      margin-bottom:0;
    }
    .info-item strong{
      color:#2563eb;
      display:block;
      margin-bottom:3px;
      font-size:0.88rem;
    }
    .risk-item{
      display:flex;
      align-items:center;
      gap:8px;
      margin-bottom:12px;
      font-size:0.85rem;
    }
    .risk-item:last-child{
      margin-bottom:0;
    }
    .risk-badge{
      display:inline-block;
      border-radius:10px;
      padding:3px 10px;
      font-weight:600;
      font-size:0.75rem;
      color:#fff;
      flex-shrink:0;
      min-width:80px;
      text-align:center;
    }
    .risk-badge.low{background:var(--low-chip);}
    .risk-badge.mid{background:var(--mid-chip);}
    .risk-badge.high{background:var(--high-chip);}

    .app-body{padding:32px;}
    .field-label{font-weight:600;font-size:0.92rem;color:#1e40af;}
    .input-group-text{background:#f8fafc;border:1px solid var(--border);color:var(--muted);font-size:0.9rem;}
    .form-control{
      background:#ffffff;
      border:1px solid var(--border);
      color:var(--text);
      transition:all 0.2s ease;
    }
    .form-control::placeholder{color:#94a3b8;}
    .form-control:focus{
      background:#ffffff;
      border-color:#3b82f6;
      box-shadow:0 0 0 .25rem rgba(59,130,246,.15);
      color:var(--text);
    }

    .btn-primary{
      background:linear-gradient(135deg,var(--brand),var(--brand-2));
      border:none;
      font-weight:700;
      padding:10px 28px;
      box-shadow:0 4px 14px rgba(30,64,175,.3);
      transition:all 0.2s ease;
    }
    .btn-primary:hover{
      filter:brightness(1.1);
      transform:translateY(-1px);
      box-shadow:0 6px 20px rgba(30,64,175,.4);
    }
    .btn-outline-secondary{
      color:var(--text);
      border-color:var(--border);
      background:#ffffff;
      padding:10px 28px;
      font-weight:600;
      transition:all 0.2s ease;
    }
    .btn-outline-secondary:hover{
      background:#f1f5f9;
      border-color:#94a3b8;
      color:var(--text);
    }

    .soft-divider{height:1px;background:var(--border);margin:1.25rem 0 1.5rem;}

    .result{
      border-radius:16px;padding:24px;
      border:1px solid var(--border);
      animation:slideIn .3s ease-out;
      margin-top:8px;
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

    <div class="main-layout">
      <div class="left-sidebar">
        <div class="sidebar-title">
          Thông tin cơ bản
        </div>
        <div class="info-item">
          <strong>Tuổi</strong>
          Tuổi mang thai
        </div>
        <div class="info-item">
          <strong>Đường huyết</strong>
          Nồng độ glucose (mmol/L)
        </div>
        <div class="info-item">
          <strong>Huyết áp tâm thu</strong>
          Áp lực khi tim co bóp (mmHg)
        </div>
        <div class="info-item">
          <strong>Huyết áp tâm trương</strong>
          Áp lực khi tim giãn nở (mmHg)
        </div>
        <div class="info-item">
          <strong>Nhịp tim</strong>
          Số nhịp tim đập mỗi phút (bpm)
        </div>
      </div>

    <div class="app-body">
      {% if error_msg %}
        <div class="alert alert-warning mb-3 py-2">{{ error_msg }}</div>
      {% endif %}

      <form method="POST" class="row g-3" novalidate>
          <div class="col-md-6">
            <label class="form-label field-label">Tuổi</label>
            <div class="input-group">
              <input type="number" name="age" min="10" max="60" required placeholder="VD: 27" class="form-control">
              <span class="input-group-text">tuổi</span>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label field-label">Nhịp tim</label>
            <div class="input-group">
              <input type="number" name="heart_rate" min="40" max="220" required placeholder="VD: 76" class="form-control">
              <span class="input-group-text">bpm</span>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label field-label">Huyết áp tâm thu</label>
            <div class="input-group">
              <input type="number" name="systolic_bp" step="0.1" min="70" max="250" required placeholder="VD: 120" class="form-control">
              <span class="input-group-text">mmHg</span>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label field-label">Huyết áp tâm trương</label>
            <div class="input-group">
              <input type="number" name="diastolic_bp" step="0.1" min="40" max="150" required placeholder="VD: 80" class="form-control">
              <span class="input-group-text">mmHg</span>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label field-label">Đường huyết</label>
            <div class="input-group">
              <input type="number" name="bs" step="0.1" min="3" max="25" required placeholder="VD: 7.5" class="form-control">
              <span class="input-group-text">mmol/L</span>
            </div>
          </div>

          <div class="col-md-6 d-flex align-items-end gap-3">
            <button type="submit" class="btn btn-primary px-4 flex-grow-1">
              Dự đoán
            </button>
            <button type="reset" class="btn btn-outline-secondary px-4">
              Xóa
            </button>
          </div>
        </form>

      {% if show_result %}
        <div class="soft-divider"></div>
        <div class="result {{ risk_class }} text-center">
          <span class="chip {{ risk_class }}">{{ result }}</span>
        </div>
      {% endif %}
    </div>

    <div class="right-sidebar">
      <div class="sidebar-title">
        Mức nguy cơ
      </div>
      <div class="risk-item">
        <span class="risk-badge low">Thấp</span>
        <span>Chỉ số bình thường</span>
      </div>
      <div class="risk-item">
        <span class="risk-badge mid">Trung bình</span>
        <span>Cần theo dõi</span>
      </div>
      <div class="risk-item">
        <span class="risk-badge high">Cao</span>
        <span>Can thiệp y tế ngay</span>
      </div>
    </div>
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

    # Lấy kết quả từ session (nếu có) rồi xóa ngay
    if 'result' in session:
        result = session.pop('result')
        risk_class = session.pop('risk_class')
        show_result = True
    
    if 'error_msg' in session:
        error_msg = session.pop('error_msg')

    if request.method == "POST":
        # Chỉ xử lý khi form có đầy đủ key
        required_keys = ("age", "systolic_bp", "diastolic_bp", "bs", "heart_rate")
        form = request.form

        missing = [k for k in required_keys if not form.get(k)]
        # Kiểm tra xem có ít nhất 1 trường được điền không
        has_any_data = any(form.get(k) for k in required_keys)
        
        if missing and has_any_data:
            # Người dùng đã submit nhưng thiếu dữ liệu
            session['error_msg'] = "Dữ liệu không hợp lệ. Vui lòng nhập lại."
            return redirect(url_for('predict'))
        elif not missing:
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
                    result_text, result_class = mapping[int(prediction)]
                    session['result'] = result_text
                    session['risk_class'] = result_class
                    return redirect(url_for('predict'))
                else:
                    session['error_msg'] = "Kết quả không xác định từ mô hình."
                    return redirect(url_for('predict'))
            except ValueError:
                # Lỗi chuyển kiểu số (nhập sai định dạng)
                session['error_msg'] = "Dữ liệu không hợp lệ. Vui lòng nhập lại."
                return redirect(url_for('predict'))
            except Exception:
                # Lỗi không mong muốn khác
                session['error_msg'] = "Đã xảy ra lỗi khi dự đoán. Vui lòng thử lại."
                return redirect(url_for('predict'))

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        risk_class=risk_class,
        error_msg=error_msg,
        show_result=show_result,
    )

if __name__ == "__main__":
    # Chạy Flask
    app.run(debug=True)
