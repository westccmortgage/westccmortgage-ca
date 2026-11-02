#!/usr/bin/env python3
"""Deterministic WCCM Before the Keys 24-second 1080x1920 video renderer."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from tempfile import TemporaryDirectory
import json, subprocess

ROOT = Path(__file__).resolve().parent
TARGET = ROOT.parent / "before-the-keys"
TARGET.mkdir(parents=True, exist_ok=True)
W,H=1080,1920
BG="#F7F6F2"; NAVY="#102036"; BLUE="#175CF2"; MUTED="#67717D"; WHITE="#FFFFFF"
FONT="/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf"
BOLD="/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf"

def f(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def width(d, s, font):
    return d.textbbox((0,0),s,font=font)[2]

def wrap(d,text,font,max_width):
    lines=[]; current=""
    for word in text.split():
        proposed=(current+" "+word).strip()
        if width(d,proposed,font)<=max_width:
            current=proposed
        elif current:
            lines.append(current);current=word
        else:
            raise ValueError("Overlong word "+word)
    if current:lines.append(current)
    return lines

def equal_housing(d,x,y):
    d.line([(x+7,y+28),(x+35,y+4),(x+65,y+28)],fill=NAVY,width=5)
    d.line([(x+18,y+22),(x+18,y+58),(x+54,y+58),(x+54,y+22)],fill=NAVY,width=5)
    d.line([(x+26,y+34),(x+46,y+34)],fill=NAVY,width=4)
    d.line([(x+26,y+44),(x+46,y+44)],fill=NAVY,width=4)
    d.text((x-20,y+73),"EQUAL HOUSING",font=f(19,True),fill=NAVY)
    d.text((x-23,y+96),"OPPORTUNITY",font=f(19,True),fill=NAVY)

def base(ep,t):
    im=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((72,90,225,148),radius=17,fill=NAVY)
    d.text((95,100),"WCCM",font=f(37,True),fill=WHITE)
    d.text((251,100),"BEFORE THE KEYS",font=f(34,True),fill=NAVY)
    d.text((72,175),f"DRAMATIZED EXAMPLE  /  EPISODE {ep['n']:02d}",font=f(24),fill=MUTED)
    for i,line in enumerate(ep["headline"]):
        sz=82
        while sz>=55 and width(d,line,f(sz,True))>925:sz-=2
        d.text((72,273+i*105),line,font=f(sz,True),fill=BLUE if i==1 else NAVY)
    d.line([(72,1508),(1008,1508)],fill="#D6D8D7",width=2)
    d.text((72,1535),"West Coast Capital Mortgage Inc.",font=f(32,True),fill=NAVY)
    d.text((72,1583),"Company NMLS #2817729",font=f(27),fill=NAVY)
    d.text((72,1621),"CA DRE Corporation License #02440065",font=f(24),fill=MUTED)
    d.text((72,1670),"Equal Credit Opportunity  |  Educational only.",font=f(21),fill=MUTED)
    d.text((72,1710),"150 E Olive Ave, Unit 112, Burbank, CA 91502",font=f(21),fill=MUTED)
    equal_housing(d,917,1522)
    d.rounded_rectangle((72,1810,1008,1818),radius=4,fill="#DDDFE3")
    d.rounded_rectangle((72,1810,max(80,int(72+936*t/24)),1818),radius=4,fill=BLUE)
    return im,d

def bubble(d,y,label,text):
    sz=40;lines=wrap(d,text,f(sz,True),826)
    while len(lines)>3 and sz>31:
        sz-=2;lines=wrap(d,text,f(sz,True),826)
    ht=96+len(lines)*50
    d.rounded_rectangle((73,y+7,1008,y+ht+7),radius=26,fill="#EDECE8")
    d.rounded_rectangle((72,y,1007,y+ht),radius=26,fill=WHITE)
    d.rounded_rectangle((72,y,82,y+ht),radius=4,fill=BLUE if label=="LOAN OFFICER" else "#AAB3C2")
    d.text((113,y+20),label,font=f(24,True),fill=BLUE if label=="LOAN OFFICER" else MUTED)
    for i,line in enumerate(lines):d.text((111,y+63+i*50),line,font=f(sz,True),fill=NAVY)
    return y+ht+16

def scene(ep,stage):
    times=[0,1.2,4.2,6.6,10.5,17.0]
    im,d=base(ep,times[stage])
    if stage<=3:
        d.text((72,505),"A CONVERSATION BEFORE THE KEYS",font=f(23,True),fill=MUTED)
        y=552
        messages=[("BUYER",ep["buyer1"]),("LOAN OFFICER",ep["lo"]),("BUYER",ep["buyer2"])]
        for who,message in messages[:stage]:y=bubble(d,y,who,message)
        if stage==0:
            d.rounded_rectangle((73,580,1008,790),radius=26,outline="#DBE3E7",width=3)
            d.text((112,652),"Here is the question...",font=f(46,True),fill="#9FA9B5")
    elif stage==4:
        d.rounded_rectangle((72,552,1007,1050),radius=27,fill=WHITE)
        d.rounded_rectangle((72,552,84,1050),radius=4,fill=BLUE)
        d.text((112,593),"THE TAKEAWAY",font=f(29,True),fill=BLUE)
        sz=55;lines=wrap(d,ep["insight"],f(sz,True),824)
        while (len(lines)>5 or len(lines)*74>315) and sz>43:
            sz-=2;lines=wrap(d,ep["insight"],f(sz,True),824)
        for i,line in enumerate(lines):
            d.text((112,675+i*68),line,font=f(sz,True),fill=NAVY)
        y=1123
        for line in wrap(d,ep["detail"],f(37),900):
            d.text((72,y),line,font=f(37),fill=NAVY);y+=53
    else:
        d.text((72,555),"ONE THING TO CHECK",font=f(32,True),fill=BLUE)
        for i,line in enumerate(wrap(d,ep["cta"],f(55,True),905)):
            d.text((72,639+i*78),line,font=f(55,True),fill=NAVY)
        d.rounded_rectangle((72,902,1008,1035),radius=27,fill=BLUE)
        d.text((119,935),"(310) 654-1577",font=f(70,True),fill=WHITE)
        d.text((72,1105),"westcoastcapitalmortgage.com",font=f(36),fill=NAVY)
        d.text((72,1175),"Questions about your mortgage? Contact WCCM.",font=f(29),fill=MUTED)
    return im

def render(ep):
    output=TARGET/f"WCCM_Before_the_Keys_{ep['n']:02d}.mp4"
    if output.exists():
        print("Already exists:", output.name, flush=True)
        return
    with TemporaryDirectory(prefix="wccm-") as tmp:
        folder=Path(tmp)
        durations=[1.2,3.0,2.4,3.9,6.5,7.0]
        rows=[]
        for i,dur in enumerate(durations):
            png=folder/f"stage_{i}.png"
            scene(ep,i).save(png,optimize=True)
            rows.extend([f"file '{png}'",f"duration {dur}"])
        rows.append(f"file '{folder/'stage_5.png'}'")
        concat=folder/"concat.txt";concat.write_text("\n".join(rows)+"\n")
        cmd=["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000","-vf","fps=24,format=yuv420p","-t","24","-c:v","libx264","-preset","medium","-crf","26","-pix_fmt","yuv420p","-c:a","aac","-b:a","64k","-movflags","+faststart","-shortest",str(output)]
        subprocess.run(cmd,check=True)
    result=json.loads(subprocess.check_output(["ffprobe","-v","quiet","-show_streams","-show_format","-of","json",str(output)]))
    assert abs(float(result["format"]["duration"])-24)<0.06
    assert any(s.get("codec_name")=="h264" and s.get("width")==1080 and s.get("height")==1920 and s.get("r_frame_rate")=="24/1" and s.get("pix_fmt")=="yuv420p" for s in result["streams"])
    assert any(s.get("codec_name")=="aac" for s in result["streams"])
    print("Rendered:",output.name,output.stat().st_size,flush=True)

if __name__=="__main__":
    for ep in json.loads((ROOT/"episodes.json").read_text()):
        render(ep)
