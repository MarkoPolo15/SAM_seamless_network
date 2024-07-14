from itertools import cycle

class DomainFetcher:
    def __init__(self, number_of_domains):
        self.number_of_domains = number_of_domains

    def get_domains(self):
        popular_domains = [
            "google.com", "facebook.com", "youtube.com", "amazon.com", "wikipedia.org",
            "twitter.com", "instagram.com", "linkedin.com", "netflix.com", "apple.com",
            "microsoft.com", "baidu.com", "yahoo.com", "whatsapp.com", "qq.com",
            "taobao.com", "tmall.com", "sohu.com", "vk.com", "live.com",
            "jd.com", "weibo.com", "360.cn", "sina.com.cn", "blogspot.com",
            "reddit.com", "aliexpress.com", "yandex.ru", "bing.com", "office.com",
            "pinterest.com", "ebay.com", "msn.com", "wordpress.com", "twitch.tv",
            "naver.com", "ok.ru", "duckduckgo.com", "vimeo.com", "github.com"
        ]

        total_domains_needed = self.number_of_domains
        all_domains = []

        domain_cycle = cycle(popular_domains)

        for _ in range(total_domains_needed):
            all_domains.append(next(domain_cycle))

        return all_domains
