# How to get the code
1. Find suspicious `.js`
   * `/js/inviteapi.min.js` has the word "invite" in it.
   * Decode `.min` file using: `https://beautifier.io/`
   * Function `makeInviteCode()` is defined. Run in console
1. Run `makeInviteCode()` in console:
```
data: "Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb /ncv/vaivgr/trarengr"
​​
enctype: "ROT13"
```
1. Google `ROT13` and use website to decode:
```
In order to generate the invite code, make a POST request to /api/invite/generate
```
1. Make `POST` request:
```
$ curl -X POST https://www.hackthebox.eu/api/invite/generate
{"success":1,"data":{"code":"SktFSVMtQURFWEstUUtZSUstUUdVWk4tUUxDWFk=","format":"encoded"},"0":200}
```
1. Decode from base64:
```
echo "SktFSVMtQURFWEstUUtZSUstUUdVWk4tUUxDWFk=" | base64 -d
RZEOC-UMIVX-REWYO-BJWZL-MNRGO
```
