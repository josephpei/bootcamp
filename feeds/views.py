from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from .models import Feed

from bootcamp.decorators import ajax_required

FEEDS_NUM_PAGES = 10


def feeds(request):
    all_feeds = Feed.get_feeds()
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'feeds/feeds.html', {
        'nbar': 'feeds',
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1
    })


def _html_feeds(last_feed, user, csrf_token, feed_source='all'):
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    html = u''
    for feed in feeds:
        html = u'{0}{1}'.format(html, render_to_string(
            'feeds/partial_feed.html',
            {
                'feed': feed,
                'user': user,
                'csrf_token': csrf_token
            }
        ))
    return html


@login_required
@ajax_required
def post(request):
    last_feed = request.POST.get('last_feed')
    user = request.user
    csrf_token = unicode(csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    post = request.POST['post']
    post = post.strip()
    print post
    if len(post) > 0:
        feed.post = post[:255]
        feed.save()
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)


def like(request):
    pass