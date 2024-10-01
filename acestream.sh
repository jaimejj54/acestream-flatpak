#! /bin/bash
ID=${1:12}
PORT=6878

if !(curl "http://127.0.0.1:$PORT/webui/api/service?method=get_version")
then
	flatpak run --branch=master --arch=x86_64 --command=acestream.engine --file-forwarding org.Acestream.engine &
fi

for i in 1 2 3 4 5 6 7 8 9 10 
do
        if (curl "http://127.0.0.1:$PORT/webui/api/service?method=get_version")
        then
                flatpak run io.mpv.Mpv --profile=acestream http://127.0.0.1:$PORT/ace/getstream?id=$ID"&"pid=$$
                break
        else
                echo $i
                sleep 2
        fi

done
echo "Couldn't run Acestream"
exit 1
