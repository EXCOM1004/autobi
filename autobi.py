import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import PhotoImage, Toplevel, Label, Button
import configparser
import os
import threading
import time
import subprocess
import sys
import signal
import platform
import base64
import hashlib
import random
import string
import smtplib
import uuid as _uuid_lib
import webbrowser  # [추가] 브라우저 실행을 위한 모듈
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# maintainner sendport

class SecurityManager:
    @staticmethod
    def get_unique_id():
        system = platform.system()
        raw_id = ""
        try:
            if system == 'Windows':
# Superpass making            
                    for p in paths:
                        if os.path.exists(p):
                            with open(p, "r") as f: raw_id += f.read().strip()
                except: pass
            

            return hashlib.sha256(raw_id.encode()).hexdigest()
        except Exception:
# Superpass encryption    
        except: return ""

    @staticmethod
# superpass decrtyption
                decrypted_bytes.append(byte ^ key[i % len(key)])
            return decrypted_bytes.decode()
        except: return "DECRYPTION_ERROR"

    @staticmethod
    def encrypt_license(data):
        salt = b'Autobi Ver 1.0'
        dk = hashlib.pbkdf2_hmac('sha512', data.encode(), salt, 100000)
        return base64.b64encode(dk).decode()

class ConfigEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autobi Ver 1.0")
        self.root.geometry("1550x800")
        
        self.filename = "margin_option.conf"

        self.help_file = "help.pdf"

        self.move_file = ".moved"
        
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.optionxform = str
        self.entries = {}
        self.fixed_descriptions = {"e_point": "[결산 프로티지]", "api_rest_time": "[API 휴식 타이밍 (초)]","limit_time":"[제한 시간 (초)]",'limit_balance':'[잔액 제한 (0=모두 사용)]','accepted_gp':'[최소 체결가 차이]','accepted_gp_limt':'[최대 체결가 차이]','raverage':'[배수]','margin_type':'[long/short/free=자동]','Stop_lose':'[스탑 로즈 >1 초과일때 ]','tracker_on':'[가격 변동 추적]','ppp':'[추적전 변동 프로티지]','tracker_confirm':'[추적 감지 횟수]','coins':'[대상 코인(대문자 입력)]','main_fiat':'[메안 화폐]','send_profit_switch':'[수익시 현물 잔고로 이동]','profit_add_per':'[이동시 잔류 비율]','Compute_accepted_gp'
:'[체결가 차이 자동 계산]','stop_per':'[변동시 중지 프로티지]','Simnulation_lqui_point':'[시뮬레이션 청산 프로티지]','volcom_switch':'[거래량 체결가 계산반영]'}
        
        self.process = None 
        self.is_running = False 
        self.is_activated = False
        self.api_ready = False
        self.header_widgets = [] 
        self.right_widgets = [] 
        self.setup_ui()
        self.setup_menu()
        self.check_license_on_startup()
        self.check_api_status()
        self.auto_load_config()

        self.start_log_monitoring(".trade.log", self.log_text)
        self.start_log_monitoring(".now_true.log", self.trade_status_text, append=False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def auto_load_config(self):
        if os.path.exists(self.filename):
            try:
                self.config.read(self.filename, encoding='utf-8')
                self.create_dynamic_widgets()
                self.filename = "margin_option.conf"
            except: pass

    def manual_load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Configuration Files", "*.conf"), ("All Files", "*.*")])
        if path:
            self.filename = path
            self.auto_load_config()

    def set_running_state(self, running):
        self.is_running = running
        state = "disabled" if running else "normal"
        self.btn_simul.config(state=state)
        self.btn_stop.config(state="normal" if running else "disabled")
        if self.is_activated and self.api_ready:
            self.btn_run.config(state=state)
        self.setup_menu()

    def open_move_fiat(self):
        # 1. 메인 다이얼로그 생성
        dialog = tk.Toplevel()
        dialog.title("자산 이동(선물 ↔ 현물)")
        dialog.geometry("300x300")

        # 2. 이동 방향 선택 (Radio Buttons)
        tk.Label(dialog, text="이동 방향 선택:", font=('Arial', 12, 'bold')).pack(pady=5)
        direction_var = tk.StringVar(value="tofuture")
        tk.Radiobutton(dialog, text="선물 잔고로 이동", variable=direction_var, value="tofuture").pack()
        tk.Radiobutton(dialog, text="현물 잔고로 이동", variable=direction_var, value="tospot").pack()

        # 3. 자산 종류 선택 (Radio Buttons)
        tk.Label(dialog, text="자산 선택:", font=('Arial', 12, 'bold')).pack(pady=5)
        asset_var = tk.StringVar(value="USDC")
        for asset in ["USDC", "USDT", "BTC"]:
            tk.Radiobutton(dialog, text=asset, variable=asset_var, value=asset).pack()

        # 4. 수량 입력
        tk.Label(dialog, text="수량 입력:", font=('Arial', 12, 'bold')).pack(pady=5)
        def validate_input(P):
            """
            Entry에 입력된 값(P)이 숫자와 단 하나의 소수점만 포함하는지 검증
            """
            if P == "": # 입력창이 비어있는 경우 허용 (삭제 시)
                return True
            
            try:
                # 입력된 문자열이 숫자로 변환 가능한지 확인 (실수 포함)
                float(P)
                # 숫자가 맞으면, 소수점이 1개 이하인지 다시 확인
                if P.count('.') <= 1:
                    return True
                else:
                    return False
            except ValueError:
                # 숫자로 변환 불가능하면(문자 등) 입력 거부
                return False

        vcmd = (root.register(validate_input), '%P')
        amount_entry = tk.Entry(dialog,validate="key", validatecommand=vcmd)
        amount_entry.pack(pady=5)

        def on_submit():
            direction = direction_var.get()
            asset = asset_var.get()
            amount = amount_entry.get()

            if not amount:
                messagebox.showwarning("경고", "수량을 입력해주세요.")
                return
            lines = open(self.api_file).read().splitlines()
            dec_api = SecurityManager.decrypt_text(lines[0]); dec_sec = SecurityManager.decrypt_text(lines[1])
            try:
                # 외부 스크립트 실행#
                subprocess.run(cmd, check=True)
                
                # .wallet 파일 읽기
                wallet_info = "파일 없음"
                if os.path.exists(".wallet"):
                    with open(".wallet", "r", encoding="utf-8") as f:
                        wallet_info = f.read().strip()

                # 결과 알림 및 창 닫기
                messagebox.showinfo("완료", f"계좌 정보: {wallet_info}\n선물 자산이 남았습니다.")
                dialog.destroy() # 다이얼로그 닫기
                
            except Exception as e:
                messagebox.showerror("오류", f"자산 이동 오류가 발생 했습니다.\n확인하여 주십시오.")
        submit_btn = tk.Button(dialog, text="자산 이동", command=on_submit, bg="#4CAF50", fg="white")
        submit_btn.pack(pady=20)

    def create_dynamic_widgets(self):
        for widget in self.scroll_frame.winfo_children(): widget.destroy()
        self.entries = {}
        if 'Option' not in self.config: return
        
        items_per_column = 20
        
        for idx, (k, v) in enumerate(self.config['Option'].items()):
            col_idx = (idx // items_per_column) * 2
            row_idx = idx % items_per_column
            
            desc = self.fixed_descriptions.get(k, k)
            tk.Label(self.scroll_frame, text=desc, width=20, anchor="w").grid(row=row_idx, column=col_idx, padx=5, pady=3)
            
            lk = k.lower().replace("_", " ")
            var = tk.StringVar()

            if lk == 'margin type':
                var.set(v); widget = ttk.Combobox(self.scroll_frame, textvariable=var, values=['free', 'long', 'short'], width=10, state="readonly")
            elif lk == '
            
            
             fiat':
                var.set(v); widget = ttk.Combobox(self.scroll_frame, textvariable=var, values=['USDT', 'USDC', 'BTC'], width=10, state="readonly")
            elif v.lower() in ['true', 'false']:
                var.set(v); widget = ttk.Combobox(self.scroll_frame, textvariable=var, values=['True', 'False'], width=10, state="readonly")
            elif v.replace('.','',1).lstrip('-').isdigit(): 
                # 소수점 정밀도 계산
                inc = 1.0
                if '.' in v:
                    try:
                        decimal_places = len(v.split('.')[1])
                        inc = 1 / (10 ** decimal_places)
                    except: inc = 1.0
                
                # [수정] 최소값(min_val)을 키 값에 따라 다르게 설정
                min_val = 1.0 # 기본값
                if k == 'api_rest_time':
                    min_val = 0.1
                elif k == 'limit_balance':
                    min_val = 0.0
                elif k == 'profit_add_per':
                    min_val = 0.0
                
                widget = tk.Spinbox(self.scroll_frame, from_=min_val, to=9999999, increment=inc, width=11)
                widget.delete(0, "end")
                
                # 파일 값과 최소값 비교하여 안전한 값 설정
                try:
                    if float(v) < min_val:
                        safe_val = str(min_val).rstrip('0').rstrip('.') if '.' in str(min_val) else str(min_val)
                    else:
                        safe_val = v
                except:
                    safe_val = str(min_val).rstrip('0').rstrip('.') if '.' in str(min_val) else str(min_val)

                widget.insert(0, safe_val)
                widget.config(textvariable=var)
                var.set(safe_val)
            else:
                var.set(v); widget = tk.Entry(self.scroll_frame, textvariable=var, width=12)
            
            widget.grid(row=row_idx, column=col_idx + 1, padx=5, pady=3)
            self.entries[k] = var

    def save_logic(self):
        if 'Option' not in self.config: self.config.add_section('Option')
        for k, v in self.entries.items(): self.config.set('Option', k, v.get())
        file_path = filedialog.asksaveasfilename(defaultextension=".conf", filetypes=[("Configuration Files", "*.conf"), ("All Files", "*.*")], initialfile=self.filename)
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f: self.config.write(f)
            messagebox.showinfo("완료", f"파일이 성공적으로 저장되었습니다:\n{os.path.basename(file_path)}")

    def save_and_run_dialog(self):
        if not self.is_activated or not self.api_ready: return
        if 'Option' not in self.config: self.config.add_section('Option')
        for k, v in self.entries.items(): self.config.set('Option', k, v.get())
        with open(self.filename, 'w', encoding='utf-8') as f: self.config.write(f)
        dialog = tk.Toplevel(self.root); dialog.title("실전 매매 주의사항"); dialog.geometry("400x250"); dialog.resizable(False, False); dialog.grab_set()
        tk.Label(dialog, text="⚠️ 주의사항", font=("Arial", 14, "bold"), fg="red", pady=10).pack()
        tk.Label(dialog, text="실전매매는 시뮬레이션과 차이점이 있으며\n모든 매매 결과와 손실은 전적으로 '사용자 책임'입니다.\n이에 동의하십니까?", font=("Arial", 11), justify="center", pady=10).pack()
        chk_var = tk.IntVar()
        def toggle_btn(): confirm_btn.config(state="normal" if chk_var.get() == 1 else "disabled")
        tk.Checkbutton(dialog, text="네, 위 내용을 확인하였으며 전적으로 동의합니다.", variable=chk_var, command=toggle_btn).pack(pady=10)
        def on_confirm():
            dialog.destroy(); self.set_running_state(True); self.run_trading_script("real")
        confirm_btn = tk.Button(dialog, text="확인 및 매매 시작", command=on_confirm, bg="#f44336", fg="white", width=20, state="disabled", pady=5); confirm_btn.pack(pady=10)

    def open_update_link(self):
        """[추가] 업데이트 링크 열기"""
        webbrowser.open("https://github.com/EXCOM1004/autobi/releases/tag/autobi")

    def setup_ui(self):
        self.btn_frame = tk.Frame(self.root, pady=10)
        self.btn_frame.pack(side="top", fill="x", padx=10)
        self.header_widgets = []
        self.right_widgets = [] 
        btn_opt = {"width": 14, "height": 1}
        self.header_widgets.append(tk.Button(self.btn_frame, text="파일 불러오기", command=self.manual_load_file, **btn_opt))
        self.header_widgets.append(tk.Button(self.btn_frame, text="다른 이름으로 저장", command=self.save_logic, **btn_opt))
        
        self.btn_simul = tk.Button(self.btn_frame, text="시뮬레이션 실행", command=self.run_simulation_direct, **btn_opt)
        self.header_widgets.append(self.btn_simul)
        
        self.btn_auth = tk.Button(self.btn_frame, text="정품 인증", command=self.open_auth_dialog, bg="green", fg="white", width=12)
        self.header_widgets.append(self.btn_auth)
        
        self.btn_run = tk.Button(self.btn_frame, text="실전 실행", command=self.save_and_run_dialog, bg="#cfd8dc", width=14, state="disabled")
        self.header_widgets.append(self.btn_run)
        
        self.btn_stop = tk.Button(self.btn_frame, text="중단", command=self.stop_process_dialog, bg="red", fg="white", width=10, state="disabled")
        self.header_widgets.append(self.btn_stop)
        self.movefiat = tk.Button(self.btn_frame, text="자산 이동(선물 ↔ 현물)", command=self.open_move_fiat, bg="#eeeeee", state="disabled", width=19)
        self.header_widgets.append(self.movefiat)
        self.btn_check_wallet = tk.Button(self.btn_frame, text="자산 확인(선물)", command=self.check_asset_logic, bg="#eeeeee", state="disabled", width=14)
        self.header_widgets.append(self.btn_check_wallet)
        
        
        self.fiat_var = tk.StringVar(value="USDT")
        self.combo_fiat = ttk.Combobox(self.btn_frame, textvariable=self.fiat_var, values=['USDT', 'USDC', 'BTC'], width=7, state="readonly")
        self.header_widgets.append(self.combo_fiat)
        
        self.lbl_wallet_val = tk.Label(self.btn_frame, text="선물 잔고: -", fg="black", font=("Arial", 12, "bold"),width=35)
        self.header_widgets.append(self.lbl_wallet_val)
        
        # [수정] 오른쪽 그룹: 업데이트 -> 도움말 -> 라이센스 순서로 배치 (reverse 처리 감안하여 순서 지정)
        self.right_widgets.append(tk.Button(self.btn_frame, text="업데이트", command=self.open_update_link, width=10)) # [추가]
        self.right_widgets.append(tk.Button(self.btn_frame, text="도움말", command=self.open_help_pdf, width=10))
        self.right_widgets.append(tk.Button(self.btn_frame, text="정보", command=self.show_license_dialog, width=10))

        self.btn_frame.bind("<Configure>", self.rearrange_header_buttons)

        self.main_paned = tk.PanedWindow(self.root, orient="horizontal", sashrelief="raised", sashwidth=4); self.main_paned.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.config_panel = tk.Frame(self.main_paned)
        self.main_paned.add(self.config_panel, width=280)
        self.config_lf = tk.LabelFrame(self.config_panel, text="설정 옵션 (퍼센티지 EX> 0.2% = 1.002, True=(참),False=(거짓))")
        self.config_lf.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.config_lf, highlightthickness=0)
        self.h_scrollbar = ttk.Scrollbar(self.config_lf, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.h_scrollbar.pack(side="right", fill="y")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.trade_status_text = tk.Text(self.config_panel, height=12, bg="#f8f9fa"); self.trade_status_text.pack(fill="x", side="bottom")
        shell_lf = tk.LabelFrame(self.main_paned, text="실행 현황 (OS Shell)"); self.main_paned.add(shell_lf, width=820); self.shell_text = tk.Text(shell_lf, bg="#0c0c0c", fg="#cccccc", font=("Consolas", 12)); self.shell_text.pack(fill="both", expand=True)
        log_lf = tk.LabelFrame(self.main_paned, text="로그 기록 시간        형태        타입        가격        지수        성공/실패 여부 "); self.main_paned.add(log_lf, width=320); self.log_text = tk.Text(log_lf, bg="#000000", fg="#00ff00", font=("Consolas", 12)); self.log_text.pack(fill="both", expand=True)

    def rearrange_header_buttons(self, event=None):
        width = self.btn_frame.winfo_width()
        if width < 50: return 
        x, y = 5, 5
        max_height = 0
        
        for widget in self.header_widgets:
            w = widget.winfo_reqwidth()
            h = widget.winfo_reqheight()
            if x + w > width and x > 5:
                x = 5
                y += max_height + 5
                max_height = 0
            widget.place(x=x, y=y)
            x += w + 5
            max_height = max(max_height, h)
            
        current_right_x = width - 5
        # 오른쪽 위젯 배치 (끝에서부터 역순으로)
        for widget in reversed(self.right_widgets):
            w = widget.winfo_reqwidth()
            h = widget.winfo_reqheight()
            if x > current_right_x - w:
                y += max_height + 5
                x = 5 
                current_right_x = width - 5
                max_height = 0
            
            widget.place(x=current_right_x - w, y=y)
            current_right_x -= (w + 5)
            max_height = max(max_height, h)

        self.btn_frame.config(height=y + max_height + 10)

    def setup_menu(self):
        self.menubar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menubar, tearoff=0); file_menu.add_command(label="파일 불러오기", command=self.manual_load_file); file_menu.add_command(label="다른 이름으로 저장", command=self.save_logic); self.menubar.add_cascade(label="파일(F)", menu=file_menu)
        run_menu = tk.Menu(self.menubar, tearoff=0); run_menu.add_command(label="시뮬레이션 시작", command=self.run_simulation_direct, state="disabled" if self.is_running else "normal")
        if self.is_activated:
            run_menu.add_command(label="실전 매매 시작", command=self.save_and_run_dialog, state="disabled" if self.is_running or not self.api_ready else "normal")
            run_menu.add_command(label="API Key 관리", command=self.open_api_dialog); run_menu.add_command(label="자산 확인(선물)", command=self.check_asset_logic, state="disabled" if self.is_running else "normal")
            run_menu.add_command(label="자산 이동(현물 ↔ 선물)", command=self.open_move_fiat)
        run_menu.add_separator(); run_menu.add_command(label="프로세스 중단", command=self.stop_process_dialog, state="normal" if self.is_running else "disabled"); self.menubar.add_cascade(label="실행(R)", menu=run_menu)
        info_menu = tk.Menu(self.menubar, tearoff=0); info_menu.add_command(label="도움말 보기", command=self.open_help_pdf); info_menu.add_command(label="프로그램 정보", command=self.show_license_dialog);info_menu.add_command(label="업데이트", command=self.open_update_link); self.menubar.add_cascade(label="정보(H)", menu=info_menu)
        self.root.config(menu=self.menubar)

    def open_auth_dialog(self):

        dialog = tk.Toplevel(self.root); dialog.title("정품 인증"); dialog.geometry("600x780")
        tk.Label(dialog, text="정품인증 절차", font=("Arial", 14, "bold"), pady=10).pack()

        info_frame = tk.LabelFrame(dialog, text="사용자 정보 (필수)", padx=10, pady=10)
        info_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(info_frame, text="사용자 이름:").grid(row=0, column=0, sticky="w", pady=2)
        var_name = tk.StringVar(); tk.Entry(info_frame, textvariable=var_name, width=30).grid(row=0, column=1, pady=2)
        tk.Label(info_frame, text="이메일 (혹은 카톡 아이디):").grid(row=1, column=0, sticky="w", pady=2)
        var_email = tk.StringVar(); tk.Entry(info_frame, textvariable=var_email, width=30).grid(row=1, column=1, pady=2)
        tk.Label(info_frame, text="전화번호 (선택):").grid(row=2, column=0, sticky="w", pady=2)
        var_phone = tk.StringVar(); tk.Entry(info_frame, textvariable=var_phone, width=30).grid(row=2, column=1, pady=2)
        consent_frame = tk.LabelFrame(dialog, text="개인정보 수집 동의", padx=10, pady=10)
        consent_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(consent_frame, text="위 정보를 메인테이너 (주)엑스컴에 인증 목적으로 수집하는 것에 동의합니까?", fg="blue").pack(anchor="w")
        var_consent = tk.IntVar(value=0)
        
        def check_inputs(*args):
            if var_name.get().strip() and var_email.get().strip():
                rb_yes.config(state="normal"); rb_no.config(state="normal")
            else:
                var_consent.set(0); rb_yes.config(state="disabled"); rb_no.config(state="disabled"); btn_req.config(state="disabled")
        var_name.trace("w", check_inputs); var_email.trace("w", check_inputs)

        def toggle_req_btn():
            btn_req.config(state="normal" if var_consent.get() == 1 else "disabled", bg="#4caf50" if var_consent.get() == 1 else "#e0e0e0")

        rb_yes = tk.Radiobutton(consent_frame, text="네, 동의합니다.", variable=var_consent, value=1, command=toggle_req_btn, state="disabled")
        rb_yes.pack(anchor="w")
        rb_no = tk.Radiobutton(consent_frame, text="아니오", variable=var_consent, value=0, command=toggle_req_btn, state="disabled")
        rb_no.pack(anchor="w")

        c1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        c2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        def send_request():

            try:
          
                    m = MIMEMultipart(); m['Subject'] = f"인증요청 - {var_name.get()}"; m.attach(MIMEText(msg_body))
                    s.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, m.as_string())
                    tk.Label(consent_frame, text="메인터이너에게 인증 요청이 완료 되었습니다.\n이 창을 닫지 말고 유지해 주세요!", fg="red").pack(anchor="w")

            except Exception as e: messagebox.showerror("전송 실패", f"오류: {e}")

        btn_req = tk.Button(dialog, text="인증 요청", command=send_request, state="disabled", width=25, height=2); btn_req.pack(pady=5)
        ttk.Separator(dialog, orient='horizontal').pack(fill='x', pady=10)

        verify_frame = tk.Frame(dialog)
        verify_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(verify_frame, text=f"요청 시리얼: {c1}", font=("Consolas", 11, "bold")).pack()
        tk.Label(verify_frame, text="인증 키 입력:", font=("Arial", 10)).pack(pady=2)
        var_key = tk.StringVar(); e_key = tk.Entry(verify_frame, textvariable=var_key, width=20, justify="center"); e_key.pack(pady=2)

        disclaimer_frame = tk.Frame(verify_frame)
        def check_key_input(*args):
            if var_key.get() == c2: disclaimer_frame.pack(pady=5, fill="x")
            else: disclaimer_frame.pack_forget()
        var_key.trace("w", check_key_input)
        tk.Label(disclaimer_frame, text="1. 실전 실행으로 인해 발생하는 모든 사항및 손실은 프로그램 사용 당사자의 책입니다.", fg="red", font=("Arial", 12, "bold")).pack()
        tk.Label(disclaimer_frame, text="2. API 방어 모듈을 지원하지만 프로그램 제작자는 API 오류시에 발생 할수 책임을 일체 지지 않습니다.", fg="red", font=("Arial", 12, "bold")).pack()
        tk.Label(disclaimer_frame, text="3. 프로그램 사용 당사자는 실전 실행 이전에 설정 옵션의 변경 및 시뮬레이션 및 연구할 스스로의 책임이 있습니다.", fg="red", font=("Arial", 12, "bold")).pack()
        tk.Label(disclaimer_frame, text="4. 시뮬레이션은 실제 매도수율에 따른 결산을 하는 것이 아니므로 \n시뮬레이션과 실전 실행의 차이점이 있음을 프로그램 사용 당사자는 인정합니다.", fg="red", font=("Arial", 12, "bold")).pack()
        tk.Label(disclaimer_frame, text="5. 본 프로그램은 실전 거래에서 청산 지정을 해주 않습니다.\n 프로그램 사용 당사자는 이를 스스로 판단할 것을 인정합니다.",  fg="red", font=("Arial", 12, "bold")).pack()
        
        var_agree_final = tk.IntVar(value=0)
        def toggle_verify_btn():
            btn_verify.config(state="normal" if var_agree_final.get() == 1 else "disabled", bg="#2196f3" if var_agree_final.get() == 1 else "#e0e0e0")
        tk.Radiobutton(disclaimer_frame, text="이를 인정합니다.", variable=var_agree_final, value=1, command=toggle_verify_btn).pack(anchor="center")
        tk.Radiobutton(disclaimer_frame, text="인정 하지 않습니다.", variable=var_agree_final, value=0, command=toggle_verify_btn).pack(anchor="center")

        def final_verify():
            if e_key.get() == c2 and var_agree_final.get() == 1:
                with open(self.license_file, 'w') as f: f.write(SecurityManager.encrypt_license(SecurityManager.get_unique_id()))
                dialog.destroy()
                self.apply_activation_ui(); messagebox.showinfo("성공", "라이센스 정품 인증이 완료 되었습니다."); 
                
            else: messagebox.showerror("실패", "인증키 오류")
        btn_verify = tk.Button(verify_frame, text="라이센스 계약 체결", command=final_verify, state="disabled", width=20); btn_verify.pack(pady=10)

    def apply_activation_ui(self):
        self.is_activated = True; self.btn_run.config(state="normal", bg="#e1f5fe"); self.btn_auth.pack_forget()
        if self.btn_auth in self.header_widgets: self.header_widgets.remove(self.btn_auth)
        self.btn_auth.destroy()
        self.lbl_auth_status = tk.Label(self.btn_frame, text="✅ 정품인증 완료", fg="#2e7d32", font=("Arial", 12, "bold"))
        self.header_widgets.insert(3, self.lbl_auth_status)
        self.btn_api_config = tk.Button(self.btn_frame, text="API KEY 추가/변경", command=self.open_api_dialog, bg="#fff9c4", font=("Arial", 12), width=18)
        self.header_widgets.append(self.btn_api_config)
        self.check_api_status(); self.setup_menu(); self.rearrange_header_buttons()

    def check_api_status(self):
        if self.is_activated and os.path.exists(self.api_file):
            self.api_ready = True; self.btn_check_wallet.config(state="normal", bg="#fff9c4")
            self.api_ready = True; self.movefiat.config(state="normal", bg="#efbbee")
            
            if hasattr(self, 'lbl_api_status'): 
                if self.lbl_api_status in self.header_widgets: self.header_widgets.remove(self.lbl_api_status)
                self.lbl_api_status.destroy()
            self.lbl_api_status = tk.Label(self.btn_frame, text="✅ API KEY 로드됨", fg="red", font=("Arial", 12, "bold"))
            self.header_widgets.append(self.lbl_api_status)
            self.setup_menu(); self.rearrange_header_buttons()

    def check_asset_logic(self):
        if not self.api_ready: return
        def run_check():
            try:
                with open(self.api_file, "r") as f: lines = f.read().splitlines()
                dec_api = SecurityManager.decrypt_text(lines[0]); dec_sec = SecurityManager.decrypt_text(lines[1])
                self.lbl_wallet_val.config(text="조회 중...", fg="orange")

                time.sleep(7)
                if os.path.exists(self.wallet_file):
                    with open(self.wallet_file, "r", encoding="utf-8") as f: balance = f.read().strip()
                    self.lbl_wallet_val.config(text=f"잔고: {balance}", fg="blue")
                else: self.lbl_wallet_val.config(text="잔고: 없음", fg="red")
            except: self.lbl_wallet_val.config(text="오류", fg="red")

        threading.Thread(target=run_check, daemon=True).start()

    def open_api_dialog(self):
        dialog = tk.Toplevel(self.root); dialog.title("API 설정"); dialog.geometry("500x300")
        tk.Label(dialog, text="바이낸스에서 발급받은 API KEY키 입력과 암호화 저장을 진행합니다.", font=("Arial", 12, "bold"), pady=15).pack()
        tk.Label(dialog,text="API KEY", fg="red", font=("Arial", 10)).pack()
        e_api = tk.Entry(dialog, width=50, justify="center"); e_api.pack(pady=5)
        tk.Label(dialog,text="SECRET KEY", fg="red", font=("Arial", 10)).pack()
        e_sec = tk.Entry(dialog, width=50, justify="center"); e_sec.pack(pady=5)
        def save():
#superpass apki making
            self.check_api_status(); dialog.destroy()
        tk.Button(dialog, text="확인", command=save, bg="#4caf50", fg="white", width=20).pack(pady=20)

    def run_simulation_direct(self): 
        if 'Option' not in self.config: self.config.add_section('Option')
        for k, v in self.entries.items(): self.config.set('Option', k, v.get())
        with open(self.filename, 'w', encoding='utf-8') as f: self.config.write(f)
        self.set_running_state(True); self.run_trading_script("simul")

    def run_trading_script(self, mode="simul"):
        self.shell_text.delete(1.0, tk.END)
        def run():
            try:
\                if mode == "real":
                    lines = open(self.api_file).read().splitlines()
                    dec_api = SecurityManager.decrypt_text(lines[0]); dec_sec = SecurityManager.decrypt_text(lines[1])
                    cmd += ["start", dec_api, dec_sec]
                else: cmd.append("simul")
                for line in iter(self.process.stdout.readline, ''): self.shell_text.insert(tk.END, line); self.shell_text.see(tk.END)
            finally: self.root.after(0, lambda: self.set_running_state(False))
        threading.Thread(target=run, daemon=True).start()

    def stop_process_dialog(self):
        if self.process and self.process.poll() is None:
            if messagebox.askokcancel("중단", "중단하시겠습니까?\n중단으로 발생하는 모든 책임은 프로그램 사용자 당사자에게 있으며\n실전 거래시 진입 거래시만 취소 됩니다."): self.trigger_ctrl_c()
        else: self.set_running_state(False)

    def trigger_ctrl_c(self):
        if self.process:
            try:
                if sys.platform == 'win32': os.kill(self.process.pid, signal.CTRL_C_EVENT)
                else: self.process.send_signal(signal.SIGINT)
            except: pass
            self.set_running_state(False)

    def on_closing(self):
        if self.process and self.process.poll() is None:
            if messagebox.askokcancel("경고", "지금 트레이딩 프로세스가 실행 중입니다. \n정말 중단 및 종료 하시겠습니까?\n중단으로 발생하는 모든 책임은 프로그램 사용자 당사자에게 있으며\n실전 거래시 진입 거래시만 취소 됩니다."):
                self.trigger_ctrl_c(); self.root.destroy()
        else: self.root.destroy()

    def check_license_on_startup(self):
        if os.path.exists(self.license_file):
            try:
                if SecurityManager.encrypt_license(SecurityManager.get_unique_id()) == open(self.license_file).read().strip(): self.apply_activation_ui()
            except: pass

    def open_help_pdf(self):
        if os.path.exists(self.help_file):
            try:
                if sys.platform == 'win32': os.startfile(self.help_file)
                elif sys.platform == 'darwin': subprocess.Popen(['open', self.help_file])
                else: subprocess.Popen(['xdg-open', self.help_file])
            except: pass
        else: messagebox.showwarning("파일 없음", "help.pdf가 없습니다.")

    def start_log_monitoring(self, path, widget, append=True):
        def watch():
            last = 0
            while True:
                if os.path.exists(path):
                    m = os.path.getmtime(path)
                    if m != last:
                        widget.delete(1.0, tk.END); widget.insert(tk.END, open(path, errors='ignore').read()); widget.see(tk.END)
                        last = m
                time.sleep(1)
        threading.Thread(target=watch, daemon=True).start()

    def show_license_dialog(self):
        title="소프트웨어 라이센스"
        popup = Toplevel()
        popup.title(title)
        # 팝업 크기 및 위치 설정 (예시)
        popup.geometry("300x500")
        image_path='autobi.png'
        image_path2='kakao.png'
        
        # 이미지 로드
        img = PhotoImage(file=image_path)
        img_label = Label(popup, image=img)
        img_label.image = img # 레퍼런스 유지
        img_label.pack(pady=10)
        message="Copyright 2026 (주)엑스컴.\nexcom2143@gmail.com\n오픈소스 라이센스:MIT Licence.\n카카오톡 아이디:\nsOSOIbci"
        
        # 메시지 레이블
        msg_label = Label(popup, text=message)
        msg_label.pack(pady=5)
        img = PhotoImage(file=image_path2)
        img_label = Label(popup, image=img)
        img_label.image = img # 레퍼런스 유지
        img_label.pack(pady=10)
        # 확인 버튼
        ok_button = Button(popup, text="확인", command=popup.destroy)
        ok_button.pack(pady=10)

        # 팝업이 메인 창 위에 오도록 설정
        popup.transient(root)
        popup.grab_set()
        root.wait_window(popup) # 팝업이 닫힐 때까지 대기

if __name__ == "__main__":
    root = tk.Tk(); app = ConfigEditorApp(root); root.mainloop()
