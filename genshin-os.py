import hashlib
import json
import time
import os

from settings import log, CONFIG, req
from notify import Notify


def hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


class Base(object):
    def __init__(self, cookies: str = None):
        if not isinstance(cookies, str):
            raise TypeError('%s want a %s but got %s' %
                            (self.__class__, type(__name__), type(cookies)))
        self._cookie = cookies

    def get_header(self):
        header = {
            'User-Agent': CONFIG.WB_USER_AGENT,
            'Referer': CONFIG.OS_REFERER_URL,
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': self._cookie
        }
        return header


class Roles(Base):
    def get_awards(self):
        response = {}
        try:
            response = req.to_python(req.request(
                'get', CONFIG.OS_REWARD_URL, headers=self.get_header()).text)
        except json.JSONDecodeError as e:
            raise Exception(e)

        return response


class Sign(Base):
    def __init__(self, cookies: str = None):
        super(Sign, self).__init__(cookies)
        self.uid = uid

    # def get_header(self): no override

    def get_info(self):
        info_url = CONFIG.OS_INFO_URL
        try:
            response = req.request(
                'get', info_url, headers=self.get_header()).text
            return req.to_python(response)
        except Exception as e:
            log.error('failure in get_info')
            raise

    def get_region_name(self):
        region_name_url = CONFIG.OS_ROLE_URL
        try:
            response = req.request(
                'get', region_name_url, headers=self.get_header()).text
            # get region_name base on highest character level in the server
            character_list = req.to_python(response).get('data',{}).get('list')
            if len(character_list) == 1:
                return character_list[0]['region_name']
            main_character_level = 0
            region_name = ''
            for data in character_list:
                if data['level'] > main_character_level:
                    main_character_level = data['level']
                    region_name = data['region_name']
            return region_name
        except Exception as e:
            log.error('failure in get_region_name')
            raise

    def run(self):
        info_list = self.get_info()
        region_name = self.get_region_name()
        message_list = []
        if info_list:
            today = info_list.get('data',{}).get('today')
            total_sign_day = info_list.get('data',{}).get('total_sign_day')
            awards = Roles(self._cookie).get_awards().get('data',{}).get('awards')
            uid = str(self.uid).replace(
                str(self.uid)[1:7], '******', 1)

            log.info(f'Checking in account id {uid}...')
            time.sleep(10)
            message = {
                'today': today,
                'region_name': region_name,
                'uid': uid,
                'total_sign_day': total_sign_day,
                'end': '',
            }
            if info_list.get('data',{}).get('is_sign') is True:
                message['award_name'] = awards[total_sign_day - 1]['name']
                message['award_cnt'] = awards[total_sign_day - 1]['cnt']
                message['status'] = f"Traveler, you've already checked in today"
                message_list.append(self.message.format(**message))
                return ''.join(message_list)
            else:
                message['award_name'] = awards[total_sign_day]['name']
                message['award_cnt'] = awards[total_sign_day]['cnt']
            if info_list.get('data',{}).get('first_bind') is True:
                message['status'] = f'Please check in manually once'
                message_list.append(self.message.format(**message))
                return ''.join(message_list)

            data = {
                'act_id': CONFIG.OS_ACT_ID
            }

            try:
                response = req.to_python(req.request(
                    'post', CONFIG.OS_SIGN_URL, headers=self.get_header(),
                    data=json.dumps(data, ensure_ascii=False)).text)
            except Exception as e:
                raise
            code = response.get('retcode', 99999)
            # 0:      success
            # -5003:  already checked in
            if code != 0:
                message_list.append(response)
                return ''.join(message_list)
            message['total_sign_day'] = total_sign_day + 1
            message['status'] = response['message']
            message_list.append(self.message.format(**message))
        log.info('Check-in complete')

        return ''.join(message_list)

    @property
    def message(self):
        return CONFIG.MESSAGE_TEMPLATE


if __name__ == '__main__':
    log.info(f'Genshin Impact Check-In Helper v{CONFIG.GIH_VERSION}')
    log.info('If you fail to check in, please try to update!')

    notify = Notify()
    msg_list = []
    ret = success_num = fail_num = 0
    """
    HoYoLAB Community's COOKIE
    :param OS_COOKIE: HoYoLAB cookie(s) for one or more accounts.
        Separate cookies for multiple accounts with the hash symbol #
        e.g. cookie1text#cookie2text
        Do not surround cookies with quotes "" if using Github Secrets.
    """
    # Github Actions -> Settings -> Secrets
    # Ensure that the Name is exactly: OS_COOKIE
    # Value should look like: login_ticket=xxx; account_id=696969; cookie_token=xxxxx; ltoken=xxxx; ltuid=696969; mi18nLang=en-us; _MHYUUID=xxx
    #         Separate cookies for multiple accounts with the hash symbol #
    #         e.g. cookie1text#cookie2text
    OS_COOKIE = ''

    if os.environ.get('OS_COOKIE', '') != '':
        OS_COOKIE = os.environ['OS_COOKIE']
    else:
        log.error("Cookie not set properly, please read the documentation on how to set and format your cookie in Github Secrets.")
        raise Exception("Cookie failure")

    cookie_list = OS_COOKIE.split('#')
    log.info(f'Number of account cookies read: {len(cookie_list)}')
    for i in range(len(cookie_list)):
        log.info(f'Preparing NO.{i + 1} Account Check-In...')
        try:
            ltoken = cookie_list[i].split('ltoken=')[1].split(';')[0]
            uid = cookie_list[i].split('account_id=')[1].split(';')[0]
            msg = f'	NO.{i + 1} Account:{Sign(cookie_list[i]).run()}'
            msg_list.append(msg)
            success_num = success_num + 1
        except Exception as e:
            msg = f'	NO.{i + 1} Account:\n    {e}'
            msg_list.append(msg)
            fail_num = fail_num + 1
            log.error(msg)
            ret = -1
        continue
    notify.send(status=f'Number of successful sign-ins: {success_num} | Number of failed sign-ins: {fail_num}', msg=msg_list)
    if ret != 0:
        log.error('program terminated with errors')
        exit(ret)
    log.info('exit success')

