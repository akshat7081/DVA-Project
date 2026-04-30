"""
Social Media Trends Analytics Dashboard
DVA Assignment 2 | Akshat Tripathi | 04914202023 | IPU BCA 6th Sem
"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import os

# MIDNIGHT PURPLE THEME
BG="#13111C"; CARD="#1E1B2E"; CARD2="#252238"; FG="#F0E6FF"
ACCENT="#B983FF"; ACCENT2="#D4BBFF"; GOOD="#00E396"; WARN="#FF6178"
MID="#FEB019"; MUTED="#8A85A0"; BORDER="#362F50"
PLATFORM_COLORS={"Twitter":"#1DA1F2","Instagram":"#E4405F","YouTube":"#FF0000","Facebook":"#1877F2","TikTok":"#25F4EE"}
CATEGORY_COLORS={"Entertainment":"#FF6B6B","Sports":"#4ECDC4","Politics":"#FFE66D","Technology":"#A29BFE","Fashion":"#FD79A8","Gaming":"#6C5CE7","Food":"#FDCB6E","Travel":"#00B894","Education":"#74B9FF","Health":"#55EFC4"}
mpl.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Segoe UI","DejaVu Sans","Arial"],"font.size":11,"axes.titlesize":13,"axes.labelsize":11,"xtick.labelsize":10,"ytick.labelsize":10,"legend.fontsize":10,"figure.facecolor":BG,"axes.facecolor":CARD,"axes.edgecolor":BORDER,"axes.labelcolor":MUTED,"xtick.color":FG,"ytick.color":FG,"text.color":FG,"grid.color":BORDER,"grid.linewidth":0.5})
DPI=100; FILE_PATH="Social_Media_Trends_India.csv"
FONT_TABLE=("Segoe UI",10); FONT_THEAD=("Segoe UI",10,"bold")

def fmt_num(n):
    n=float(n)
    if n>=1e6: return f"{n/1e6:.1f}M"
    if n>=1e3: return f"{n/1e3:.1f}K"
    return str(int(n))

def load_data():
    df=pd.read_csv(FILE_PATH); df.columns=[c.strip().lower() for c in df.columns]; return df

def style_ax(ax,title="",xlabel="",ylabel=""):
    ax.set_facecolor(CARD)
    for sp in ax.spines.values(): sp.set_color(BORDER)
    ax.tick_params(axis="x",colors=FG); ax.tick_params(axis="y",colors=FG)
    if title: ax.set_title(title,color=ACCENT2,fontsize=12,fontweight="bold",pad=8)
    if xlabel: ax.set_xlabel(xlabel,color=MUTED)
    if ylabel: ax.set_ylabel(ylabel,color=MUTED)

def fix_yticks(ax,fs=10): ax.tick_params(axis="y",labelrotation=0,labelsize=fs,colors=FG)
def trunc(s,n=14): s=str(s); return s if len(s)<=n else s[:n-1]+"..."

def hbar(ax,labels,values,colors,fs=10,bh=0.65,vlabels=True):
    bars=ax.barh(labels,values,color=colors,height=bh,edgecolor=BORDER,linewidth=0.5)
    if vlabels: ax.bar_label(bars,fmt="%.1f",color=FG,fontsize=fs-1,padding=3)
    fix_yticks(ax,fs); return bars

def embed(fig,parent):
    c=FigureCanvasTkAgg(fig,master=parent); c.draw(); c.get_tk_widget().pack(fill="both",expand=True)

def page_header(p,title,sub=""):
    hf=tk.Frame(p,bg=CARD,highlightbackground=ACCENT,highlightthickness=2)
    hf.pack(fill="x",padx=18,pady=(12,6))
    tk.Label(hf,text=title,bg=CARD,fg=ACCENT2,font=("Segoe UI",18,"bold")).pack(anchor="w",padx=16,pady=(10,2))
    if sub: tk.Label(hf,text=sub,bg=CARD,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",padx=16,pady=(0,8))

def cell_tc(cmap,nv):
    if nv is None or (isinstance(nv,float) and np.isnan(nv)): return FG
    rgba=cmap(float(nv)); lum=0.299*rgba[0]+0.587*rgba[1]+0.114*rgba[2]
    return "black" if lum>0.50 else "white"

def scrollable_table(parent,hdrs,cwidths,rows_data,row_colors_fn):
    fr=tk.Frame(parent,bg=CARD,highlightbackground=ACCENT,highlightthickness=1)
    fr.pack(side="left",fill="both",expand=True,padx=(0,10))
    cv=tk.Canvas(fr,bg=CARD,highlightthickness=0)
    vs=ttk.Scrollbar(fr,orient="vertical",command=cv.yview)
    vs.pack(side="right",fill="y"); cv.pack(side="left",fill="both",expand=True)
    cv.configure(yscrollcommand=vs.set)
    inner=tk.Frame(cv,bg=CARD); win=cv.create_window((0,0),window=inner,anchor="nw")
    inner.bind("<Configure>",lambda e:cv.configure(scrollregion=cv.bbox("all")))
    cv.bind("<Configure>",lambda e:cv.itemconfig(win,width=max(e.width,inner.winfo_reqwidth())))
    cv.bind("<MouseWheel>",lambda e:cv.yview_scroll(int(-1*(e.delta/120)),"units"))
    for i,(h,w) in enumerate(zip(hdrs,cwidths)):
        tk.Label(inner,text=h,bg=BORDER,fg=ACCENT,font=FONT_THEAD,width=w,anchor="w").grid(row=0,column=i,padx=8,pady=10,sticky="we")
    for ridx,vals in enumerate(rows_data,1):
        cbg=CARD2 if ridx%2==0 else CARD
        for cidx,(val,w) in enumerate(zip(vals,cwidths)):
            col=row_colors_fn(ridx,cidx,val)
            tk.Label(inner,text=val,bg=cbg,fg=col,font=FONT_TABLE,width=w,anchor="w").grid(row=ridx,column=cidx,padx=8,pady=7,sticky="we")

def build_dashboard(root,df):
    # HEADER with accent border
    hdr=tk.Frame(root,bg=CARD,highlightbackground=ACCENT,highlightthickness=2)
    hdr.pack(fill="x",padx=16,pady=(10,4))
    lh=tk.Frame(hdr,bg=CARD); lh.pack(side="left",padx=14,pady=10)
    tk.Label(lh,text="Social Media Trends Analytics Dashboard",bg=CARD,fg=FG,font=("Segoe UI",22,"bold")).pack(anchor="w")
    tk.Label(lh,bg=CARD,fg=MUTED,font=("Segoe UI",10),text=f"{len(df)} Records  |  {df['platform'].nunique()} Platforms  |  {df['category'].nunique()} Categories  |  {df['country'].nunique()} Countries").pack(anchor="w")
    rh=tk.Frame(hdr,bg=CARD); rh.pack(side="right",padx=14,pady=10)
    tk.Label(rh,text="DVA Assignment 2",bg=CARD,fg=ACCENT,font=("Segoe UI",12,"bold")).pack(anchor="e")
    tk.Label(rh,text="Akshat Tripathi | 04914202023",bg=CARD,fg=ACCENT2,font=("Segoe UI",10,"bold")).pack(anchor="e")
    tk.Label(rh,text="IPU BCA 6th Semester",bg=CARD,fg=MUTED,font=("Segoe UI",9)).pack(anchor="e")

    # NOTEBOOK
    st=ttk.Style(); st.theme_use("default")
    st.configure("TNotebook",background=BG,borderwidth=0)
    st.configure("TNotebook.Tab",background=CARD,foreground=FG,padding=(28,11),font=("Segoe UI",11,"bold"))
    st.map("TNotebook.Tab",background=[("selected","#B983FF")],foreground=[("selected","#13111C")])
    nb=ttk.Notebook(root,style="TNotebook"); nb.pack(fill="both",expand=True,padx=12,pady=8)
    page1(nb,df); page2(nb,df); page3(nb,df); page4(nb,df); page5(nb,df)

def page1(nb,df):
    p=tk.Frame(nb,bg=BG); nb.add(p,text="  Overview  ")
    body=tk.Frame(p,bg=BG); body.pack(fill="both",expand=True)
    left=tk.Frame(body,bg=BG,width=300); left.pack(side="left",fill="y",padx=(8,6),pady=8); left.pack_propagate(False)
    kpis=[
        ("Total Posts",fmt_num(df["posts"].sum()),"All platforms combined",ACCENT),
        ("Total Views",fmt_num(df["views"].sum()),"Combined reach",ACCENT2),
        ("Total Likes",fmt_num(df["likes"].sum()),"User reactions",GOOD),
        ("Avg Engagement",f"{df['engagement_rate'].mean():.2f}%","(Likes+Cmts+Shares)/Views",MID),
        ("Top Platform",df.groupby("platform")["views"].sum().idxmax(),"By total views",PLATFORM_COLORS.get(df.groupby("platform")["views"].sum().idxmax(),FG)),
        ("Trending Category",df.groupby("category")["engagement_rate"].mean().idxmax(),"Highest avg engagement",WARN),
    ]
    for title,val,sub,c in kpis:
        card=tk.Frame(left,bg=CARD,padx=12,pady=8,highlightbackground=BORDER,highlightthickness=1); card.pack(fill="x",pady=3)
        tk.Label(card,text=title,bg=CARD,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w")
        tk.Label(card,text=val,bg=CARD,fg=c,font=("Segoe UI",15,"bold")).pack(anchor="w")
        if sub: tk.Label(card,text=sub,bg=CARD,fg=BORDER,font=("Segoe UI",8)).pack(anchor="w")
    right=tk.Frame(body,bg=BG); right.pack(side="left",fill="both",expand=True,padx=(8,18),pady=8)
    fig=Figure(figsize=(10.5,5.5),dpi=DPI); fig.patch.set_facecolor(BG)
    gs=GridSpec(2,2,figure=fig,hspace=0.50,wspace=0.40)
    ax1=fig.add_subplot(gs[0,0])
    pv=df.groupby("platform")["views"].sum().sort_values()
    hbar(ax1,pv.index,pv.values/1e6,[PLATFORM_COLORS.get(p,ACCENT) for p in pv.index],fs=9,bh=0.55,vlabels=False)
    style_ax(ax1,"Platform Reach (Million Views)")
    ax2=fig.add_subplot(gs[1,0])
    cat_cnt=df["category"].value_counts(); clrs=[CATEGORY_COLORS.get(c,ACCENT) for c in cat_cnt.index]
    wedges,_,autotexts=ax2.pie(cat_cnt.values,colors=clrs,autopct=lambda p:f"{p:.0f}%" if p>=5 else "",pctdistance=0.75,startangle=90,wedgeprops=dict(width=0.45,edgecolor=BG,linewidth=2.5),radius=0.80)
    for at,wdg in zip(autotexts,wedges):
        fc=wdg.get_facecolor(); lum=0.299*fc[0]+0.587*fc[1]+0.114*fc[2]
        at.set_fontsize(8); at.set_fontweight("bold"); at.set_color("black" if lum>0.5 else "white")
    ax2.legend(wedges,[f"{c}({n})" for c,n in cat_cnt.items()],loc="upper center",bbox_to_anchor=(0.5,0.0),ncol=2,fontsize=7,labelcolor=FG,facecolor=CARD,edgecolor=BORDER)
    ax2.set_title("Category Distribution",color=ACCENT2,fontsize=11,fontweight="bold",pad=8)
    ax3=fig.add_subplot(gs[0,1])
    ht=df.groupby("hashtag")["views"].sum().nlargest(5).sort_values()
    hbar(ax3,ht.index,ht.values/1e6,[ACCENT]*5,fs=9,bh=0.6)
    style_ax(ax3,"Top 5 Hashtags (M Views)")
    ax4=fig.add_subplot(gs[1,1])
    pe=df.groupby("platform")["engagement_rate"].mean().sort_values()
    hbar(ax4,pe.index,pe.values,[PLATFORM_COLORS.get(p,ACCENT) for p in pe.index],fs=9,bh=0.55)
    ax4.axvline(3,color=MID,lw=1.3,ls="--",label="Avg 3%"); ax4.legend(fontsize=8,labelcolor=FG,facecolor=CARD,edgecolor=BORDER)
    style_ax(ax4,"Avg Engagement Rate (%)")
    fig.tight_layout(pad=1.5); embed(fig,right)

def page2(nb,df):
    p=tk.Frame(nb,bg=BG); nb.add(p,text="  Platform Analysis  ")
    page_header(p,"Platform-wise Social Media Performance","Detailed metrics comparison across all 5 platforms")
    body=tk.Frame(p,bg=BG); body.pack(fill="both",expand=True,padx=16,pady=6)
    plat_df=df.groupby("platform").agg(posts=("posts","sum"),likes=("likes","sum"),views=("views","sum"),comments=("comments","sum"),shares=("shares","sum"),avg_eng=("engagement_rate","mean")).reset_index().sort_values("views",ascending=False)
    hdrs=["PLATFORM","POSTS","LIKES","VIEWS","COMMENTS","SHARES","ENG%"]; cw=[14,11,11,12,11,11,9]
    rows=[[r["platform"],fmt_num(r["posts"]),fmt_num(r["likes"]),fmt_num(r["views"]),fmt_num(r["comments"]),fmt_num(r["shares"]),f"{r['avg_eng']:.2f}%"] for _,r in plat_df.iterrows()]
    def colorfn(ri,ci,val): return PLATFORM_COLORS.get(str(val),FG) if ci==0 else FG
    scrollable_table(body,hdrs,cw,rows,colorfn)
    ch=tk.Frame(body,bg=BG); ch.pack(side="left",fill="both",expand=True)
    fig=Figure(figsize=(8.5,6.0),dpi=DPI); fig.patch.set_facecolor(BG)
    gs=GridSpec(2,2,figure=fig,hspace=0.65,wspace=0.46)
    plats=plat_df["platform"]; clrs=[PLATFORM_COLORS.get(p,ACCENT) for p in plats]
    for i,(col,title) in enumerate([("likes","Likes (M)"),("shares","Shares (M)"),("comments","Comments (M)"),("avg_eng","Avg Eng %")]):
        ax=fig.add_subplot(gs[i//2,i%2])
        vals=plat_df[col]/1e6 if col!="avg_eng" else plat_df[col]
        ax.bar(plats,vals,color=clrs,edgecolor=BORDER,linewidth=0.5); style_ax(ax,title); ax.tick_params(axis="x",rotation=15,colors=FG)
    fig.subplots_adjust(left=0.12,right=0.97,top=0.94,bottom=0.12); embed(fig,ch)

def page3(nb,df):
    p=tk.Frame(nb,bg=BG); nb.add(p,text="  Category Trends  ")
    page_header(p,"Content Category Performance Analysis","Engagement and reach metrics by content category")
    fig=Figure(figsize=(12,6.5),dpi=DPI); fig.patch.set_facecolor(BG)
    gs=GridSpec(2,2,figure=fig,hspace=0.50,wspace=0.35)
    cat_df=df.groupby("category").agg(views=("views","sum"),eng=("engagement_rate","mean")).sort_values("views",ascending=False)
    ax1=fig.add_subplot(gs[0,0])
    ax1.barh(cat_df.index,cat_df["views"]/1e6,color=[CATEGORY_COLORS.get(c,ACCENT) for c in cat_df.index],height=0.6,edgecolor=BORDER,linewidth=0.5)
    style_ax(ax1,"Views by Category (M)"); fix_yticks(ax1,9)
    ax2=fig.add_subplot(gs[0,1])
    ce=cat_df.sort_values("eng"); ax2.barh(ce.index,ce["eng"],color=[CATEGORY_COLORS.get(c,ACCENT) for c in ce.index],height=0.6,edgecolor=BORDER,linewidth=0.5)
    ax2.axvline(3,color=MID,lw=1.3,ls="--"); style_ax(ax2,"Avg Engagement Rate (%)"); fix_yticks(ax2,9)
    ax3=fig.add_subplot(gs[1,0])
    ht=df.groupby("hashtag")["engagement_rate"].mean().nlargest(10).sort_values()
    ax3.barh(ht.index,ht.values,color=[ACCENT2]*10,height=0.6,edgecolor=BORDER,linewidth=0.5); style_ax(ax3,"Top 10 Hashtags by Eng Rate"); fix_yticks(ax3,8)
    ax4=fig.add_subplot(gs[1,1])
    cat_posts=df["category"].value_counts(); clrs=[CATEGORY_COLORS.get(c,ACCENT) for c in cat_posts.index]
    wedges,_,ats=ax4.pie(cat_posts.values,colors=clrs,autopct=lambda p:f"{p:.0f}%" if p>=5 else "",pctdistance=0.75,startangle=90,wedgeprops=dict(width=0.45,edgecolor=BG,linewidth=2),radius=0.80)
    for at,wdg in zip(ats,wedges):
        fc=wdg.get_facecolor(); lum=0.299*fc[0]+0.587*fc[1]+0.114*fc[2]; at.set_fontsize(8); at.set_fontweight("bold"); at.set_color("black" if lum>0.5 else "white")
    ax4.set_title("Posts per Category",color=ACCENT2,fontsize=11,fontweight="bold",pad=8)
    ax4.legend(wedges,cat_posts.index,loc="upper center",bbox_to_anchor=(0.5,0.0),ncol=2,fontsize=7,labelcolor=FG,facecolor=CARD,edgecolor=BORDER)
    fig.subplots_adjust(left=0.18,right=0.96,top=0.92,bottom=0.08); embed(fig,p)

def page4(nb,df):
    p=tk.Frame(nb,bg=BG); nb.add(p,text="  Hashtag Rankings  ")
    page_header(p,"Hashtag Performance Rankings","Top and bottom performing hashtags by total views")
    outer=tk.Frame(p,bg=BG); outer.pack(fill="both",expand=True,padx=16,pady=6)
    ht_df=df.groupby("hashtag").agg(category=("category","first"),views=("views","sum"),likes=("likes","sum"),eng=("engagement_rate","mean"),posts=("posts","sum")).reset_index().sort_values("views",ascending=False).reset_index(drop=True)
    hdrs=["#","HASHTAG","CATEGORY","VIEWS","LIKES","ENG%","POSTS"]; cw=[4,16,14,11,11,9,11]
    rows=[[i+1,r["hashtag"],r["category"],fmt_num(r["views"]),fmt_num(r["likes"]),f"{r['eng']:.2f}%",fmt_num(r["posts"])] for i,(_,r) in enumerate(ht_df.iterrows())]
    def colorfn(ri,ci,val):
        if ci==0: return MUTED
        if ci==2: return CATEGORY_COLORS.get(str(val),FG)
        return FG
    scrollable_table(outer,hdrs,cw,rows,colorfn)
    frr=tk.Frame(outer,bg=CARD,highlightbackground=ACCENT,highlightthickness=1); frr.pack(side="left",fill="both",expand=True)
    fig=Figure(figsize=(6.8,6.0),dpi=DPI); fig.patch.set_facecolor(CARD)
    ax1=fig.add_subplot(211); ax1.set_facecolor(CARD)
    t10=ht_df.head(10).sort_values("views"); hbar(ax1,t10["hashtag"],t10["views"]/1e6,[WARN]*10,fs=9,bh=0.60,vlabels=False)
    ax1.set_title("[HIGH] Top 10 Most Viewed",color=ACCENT2,fontsize=10,fontweight="bold",pad=6); fix_yticks(ax1,9)
    ax2=fig.add_subplot(212); ax2.set_facecolor(CARD)
    b10=ht_df.tail(10).sort_values("views",ascending=False); hbar(ax2,b10["hashtag"],b10["views"]/1e6,[GOOD]*10,fs=9,bh=0.60,vlabels=False)
    ax2.set_title("[LOW] Bottom 10 Least Viewed",color=ACCENT2,fontsize=10,fontweight="bold",pad=6); fix_yticks(ax2,9)
    fig.subplots_adjust(left=0.32,right=0.96,top=0.92,bottom=0.08,hspace=0.60); embed(fig,frr)

def page5(nb,df):
    p=tk.Frame(nb,bg=BG); nb.add(p,text="  Heatmap & Correlation  ")
    page_header(p,"Metric Correlation & Platform x Category Heatmap","Left: inter-metric correlation  |  Right: normalised engagement heatmap")
    fig=Figure(figsize=(12,5.8),dpi=DPI); fig.subplots_adjust(left=0.10,right=0.96,top=0.88,bottom=0.18,wspace=0.35); fig.patch.set_facecolor(BG)
    cols=["posts","likes","views","comments","shares","engagement_rate"]; lbls=["Posts","Likes","Views","Comments","Shares","Eng Rate"]
    corr=df[cols].corr()
    ax1=fig.add_subplot(121)
    im1=ax1.imshow(corr.values,cmap="PuOr",vmin=-1,vmax=1,aspect="auto")
    ax1.set_xticks(range(len(lbls))); ax1.set_xticklabels(lbls,rotation=35,ha="right",fontsize=10,color=FG)
    ax1.set_yticks(range(len(lbls))); ax1.set_yticklabels(lbls,fontsize=10,color=FG)
    cmap1=plt.get_cmap("PuOr")
    for i in range(len(lbls)):
        for j in range(len(lbls)):
            v=corr.values[i,j]; tc=cell_tc(cmap1,(v+1)/2)
            ax1.text(j,i,f"{v:.2f}",ha="center",va="center",fontsize=10,fontweight="bold",color=tc)
    cb1=fig.colorbar(im1,ax=ax1,shrink=0.80); cb1.ax.yaxis.set_tick_params(color=FG,labelsize=10); plt.setp(cb1.ax.yaxis.get_ticklabels(),color=FG)
    style_ax(ax1,"Metric Correlation Matrix")
    pivot=df.pivot_table(index="platform",columns="category",values="engagement_rate",aggfunc="mean")
    norm=(pivot-pivot.min())/(pivot.max()-pivot.min())
    ax2=fig.add_subplot(122)
    cmap2=plt.get_cmap("magma")
    im2=ax2.imshow(norm.values,cmap="magma",aspect="auto",vmin=0,vmax=1)
    ax2.set_xticks(range(len(pivot.columns))); ax2.set_xticklabels([trunc(c,9) for c in pivot.columns],fontsize=9,color=FG,rotation=35,ha="right")
    ax2.set_yticks(range(len(pivot.index))); ax2.set_yticklabels(pivot.index,fontsize=10,color=FG)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            rv=pivot.values[i,j]; nv=norm.values[i,j]
            txt="nan" if (isinstance(rv,float) and np.isnan(rv)) else f"{rv:.1f}"
            tc=cell_tc(cmap2,None if (isinstance(nv,float) and np.isnan(nv)) else nv)
            ax2.text(j,i,txt,ha="center",va="center",fontsize=9,color=tc)
    cb2=fig.colorbar(im2,ax=ax2,shrink=0.80); cb2.ax.yaxis.set_tick_params(color=FG,labelsize=10); plt.setp(cb2.ax.yaxis.get_ticklabels(),color=FG)
    style_ax(ax2,"Platform x Category Engagement")
    embed(fig,p)

def main():
    root=tk.Tk(); root.title("Social Media Trends Dashboard - Akshat Tripathi | 04914202023")
    root.configure(bg=BG); root.state("zoomed")
    df=load_data(); build_dashboard(root,df); root.mainloop()

if __name__=="__main__":
    main()
